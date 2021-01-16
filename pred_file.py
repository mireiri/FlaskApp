import pandas as pd
from sklearn.linear_model import LinearRegression
import openpyxl


def pred_file(files):
    study_file_list = [i for i in files if not 'predict' in i]
    predict_file_list = [i for i in files if 'predict' in i]
    predict_file = predict_file_list[0]
    pred_df = pd.read_excel(predict_file)
    X_pred = pred_df[['PAX']]

    df = pd.DataFrame()
    for i in study_file_list:
        raw_df = pd.read_excel(i)
        df = pd.concat([df, raw_df])

    X = df[['PAX']]
    y = df['WGT']

    lr = LinearRegression()
    lr.fit(X, y)
    result = lr.predict(X_pred)
    pred_df['WGT'] = result

    predict_file_path = 'download/' + predict_file[7:] + '_result.xlsx'
    pred_df.to_excel(predict_file_path)

    workbook = openpyxl.load_workbook(predict_file_path)
    worksheet = workbook.worksheets[0]
    worksheet.delete_cols(1)

    for cols in worksheet.iter_rows(min_row=2, min_col=1, max_col=1):
        for cell in cols:
            cell.number_format = 'YYYY/MM/DD'   
    
    workbook.save(predict_file_path)

    return predict_file_path[9:]

if __name__ == '__main__':
    files = ['static/data.xlsx', 'static/data2.xlsx', 'static/predict.xlsx']
    result = pred_file(files)
    print(result)