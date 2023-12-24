import xmltodict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class LivesplitData:
    def __init__(self, fpath):
        with open(fpath, 'r') as f:
            xml_dict = xmltodict.parse(f.read())['Run']

        self.num_attempts = int(xml_dict['AttemptCount'])
        self.num_completed_attempts = self.__compute_finished_runs_count(xml_dict)
        self.percent_runs_completed = self.num_completed_attempts / self.num_attempts * 100
        self.attempt_info_df = self.__parse_attempt_data(xml_dict)
        self.split_info_df = self.__parse_segment_data(xml_dict, self.attempt_info_df)


    
    ##################### CLASS HELPER FUNCTIONS ##############
    def __compute_finished_runs_count(self, data):
        finished_count = 0

        for d in data['AttemptHistory']['Attempt']:
            if 'RealTime' in d:
                finished_count += 1
        
        return finished_count

    def __parse_attempt_data(self, data):
        # initial data parsing
        attempt_info_df = pd.DataFrame(data['AttemptHistory']['Attempt'])
        attempt_info_df.columns = ['id', 'started', 'isStartedSynced', 'ended', 'isEndedSynced', 'RealTime']
        attempt_info_df['id'] = attempt_info_df['id'].astype(int)
        attempt_info_df['started'] = pd.to_datetime(attempt_info_df['started'], format='%m/%d/%Y %H:%M:%S')
        attempt_info_df['ended'] = pd.to_datetime(attempt_info_df['ended'], format='%m/%d/%Y %H:%M:%S')
        attempt_info_df.set_index('id', inplace=True)

        # compute time attempt lasted for
        run_finished = []

        for i in attempt_info_df.index:
            if pd.isna(attempt_info_df['RealTime'][i]):
                run_finished.append('False')
                attempt_info_df.loc[i, 'RealTime'] = attempt_info_df['ended'][i] - attempt_info_df['started'][i]
            else:
                run_finished.append('True')
        attempt_info_df['RunCompleted'] = run_finished
        attempt_info_df['RealTime'] = pd.to_timedelta(attempt_info_df['RealTime'])
        attempt_info_df['RealTime'] = attempt_info_df['RealTime'].astype(str).apply(lambda x: str(x).split()[-1])
        # attempt_info_df['RealTime'] = pd.to_timedelta(attempt_info_df['RealTime'])
        attempt_info_df = attempt_info_df[['started', 'isStartedSynced', 'ended', 'isEndedSynced', 'RunCompleted', 'RealTime']]

        # pull segment history data
        # start by getting the index values (from the attempt_history_df)
        idx = list(attempt_info_df.index)

        # next, get the column values
        col_names = []

        for d in data['Segments']['Segment']:
            col_names.append(d['Name'])

        # now create an empty DataFrame
        segment_history_df = pd.DataFrame(index=idx, columns=col_names)
        segment_history_df

        for d in data['Segments']['Segment']:
            seg_name = d['Name']

            for t in d['SegmentHistory']['Time']:
                # print(t)
                try:
                    segment_history_df.loc[int(t['@id']), seg_name] = t['RealTime']
                except:
                    pass

        segment_history_df = segment_history_df.sort_index()

        # merge segent history into attempt history dataframe
        attempt_info_df = pd.merge(attempt_info_df, segment_history_df, left_index = True, right_index=True, how='outer')

        return attempt_info_df

    def __parse_segment_data(self, data, attempt_info_df):
        # initial data pull
        segment_info_df = pd.DataFrame(data['Segments']['Segment'])
        segment_info_df.set_index('Name', inplace=True)
        segment_info_df.drop('Icon', axis=1, inplace=True)

        # pop out personal best column
        pb = []

        for i in segment_info_df.index:
            if 'RealTime' in segment_info_df['SplitTimes'][i]['SplitTime']:
                pb.append(segment_info_df['SplitTimes'][i]['SplitTime']['RealTime'])
            else:
                pb.append(np.nan)

        segment_info_df['PersonalBest'] = pb

        # pop out best segments column
        best_seg = []

        for i in segment_info_df.index:
            best_seg.append(segment_info_df['BestSegmentTime'][i]['RealTime'])

        segment_info_df['BestSegment'] = best_seg

        # compute total number of attempts that completed said split
        split_count = []
        split_percentage = []

        for i in segment_info_df.index:
            split_count.append(attempt_info_df[i].count())
            split_percentage.append(attempt_info_df[i].count() / self.num_attempts * 100)

        segment_info_df['NumRunsPassed'] = split_count
        segment_info_df['PercentRunsPassed'] = split_percentage

        segment_info_df

        # compute average splits
        avg_splits = []

        for i in segment_info_df.index:
            avg_splits.append(pd.to_timedelta(attempt_info_df[i]).mean())

        segment_info_df['Average'] = avg_splits
        segment_info_df['Average'] = segment_info_df['Average'].astype(str).apply(lambda x: str(x).split()[-1])

        # compute median splits
        med_splits = []

        for i in segment_info_df.index:
            med_splits.append(pd.to_timedelta(attempt_info_df[i]).median())

        segment_info_df['Median'] = med_splits
        segment_info_df['Median'] = segment_info_df['Median'].astype(str).apply(lambda x: str(x).split()[-1])

        # compute columns with actual split times
        def round_time(string):
            digit = int(string[string.find('.')+5])

            if digit >= 5:
                return string[:string.find('.')+5] + str(digit+1)
            else:
                return string[:string.find('.')+6]
            
        cols = ['PersonalBest', 'BestSegment', 'Average', 'Median']

        for i in segment_info_df.index:
            for c in cols:
                if not pd.isna(segment_info_df[c][i]):
                    segment_info_df.loc[i, c] = round_time(segment_info_df[c][i])

        def compute_split_times(df, col_name):
            idx = list(df.index)
            segment_times = []
            time_format = '%H:%M:%S.%f'

            first_time = df[col_name][idx[0]]
            segment_times.append(first_time)
            sum_time = datetime.strptime(first_time, time_format)

            for i in range(1, len(idx)):
                curr_time = datetime.strptime(df[col_name][idx[i]], time_format)
                sum_time += timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=curr_time.second, microseconds=curr_time.microsecond)
                segment_times.append(sum_time.strftime(time_format))
            
            df[col_name+'SplitTime'] = segment_times

            return df

        def compute_pb_segments(df):
            idx = list(df.index)
            segment_times = []
            time_format = '%H:%M:%S.%f'

            first_time = df['PersonalBest'][idx[0]]
            segment_times.append(first_time)

            for i in range(1, len(idx)):
                curr_split_time = df['PersonalBest'][idx[i]]
                
                if pd.isna(curr_split_time):
                    segment_times.append(curr_split_time)
                
                else:
                    curr_split_time = datetime.strptime(curr_split_time, time_format)
                    for j in segment_times:
                        if not pd.isna(j):
                            temp = datetime.strptime(j, time_format)
                            curr_split_time -= timedelta(hours=temp.hour, minutes=temp.minute, seconds=temp.second, microseconds=temp.microsecond)

                    segment_times.append(curr_split_time.strftime(time_format))

            df['PersonalBestSplitTime'] = segment_times

            return df

        segment_info_df = compute_pb_segments(segment_info_df)
        segment_info_df = compute_split_times(segment_info_df, 'BestSegment')
        segment_info_df = compute_split_times(segment_info_df, 'Average')
        segment_info_df = compute_split_times(segment_info_df, 'Median')

        # clean final dataframe
        segment_info_df.drop(['SplitTimes', 'BestSegmentTime', 'SegmentHistory'], axis=1, inplace=True)
        segment_info_df.rename(columns={'PersonalBest':'PersonalBestSplitTime', 'PersonalBestSplitTime':'PersonalBest'}, inplace=True)
        segment_info_df = segment_info_df[['PersonalBest', 'PersonalBestSplitTime', 'BestSegment', 'BestSegmentSplitTime', 'Average', 'AverageSplitTime', 'Median', 'MedianSplitTime', 'NumRunsPassed', 'PercentRunsPassed']]

        return segment_info_df