import pandas as pd
import openpyxl


def pd_merge(files):
    file_list = [i for i in files if not 'predict' in i]

    merge_files = '&'.join(file_list)
    merge_files = merge_files.replace('static/', '')

    df = pd.DataFrame()
    for i in file_list:
        raw_df = pd.read_excel(i)
        df = pd.concat([df, raw_df])
    
    merge_file_path = 'download/' + merge_files + '_merge.xlsx'
    df.to_excel(merge_file_path)

    workbook = openpyxl.load_workbook(merge_file_path)
    worksheet = workbook.worksheets[0]
    worksheet.delete_cols(1)

    for cols in worksheet.iter_rows(min_row=2, min_col=1, max_col=1):
        for cell in cols:
            cell.number_format = 'YYYY/MM/DD'   
    
    workbook.save(merge_file_path)

    return merge_file_path[9:]


if __name__ == '__main__':
    files = ['static/data.xlsx', 'static/data2.xlsx', 'static/predict.xlsx']
    result = pd_merge(files)
    print(result)
