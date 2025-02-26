import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('latest_sorted.csv')

# 첫 번째 열과 네 번째 열 추출
selected_columns = df.iloc[:, [0, 3]]  # 0은 첫 번째 열, 3은 네 번째 열

# 텍스트 파일로 데이터 저장 (쉼표로 구분)
selected_columns.to_csv('proxyip.txt', index=False, header=False, sep='#')
