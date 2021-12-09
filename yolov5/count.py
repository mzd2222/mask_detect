import pandas as pd
path = './runs/detect/exp12/labels/'
ans = []
for i in range(200):
    file_name = str(i) + '.txt'
    with open(path + file_name) as f:
        data = f.readlines()
        with_mask = 0
        without_mask = 0
        mask_weared_incorrect = 0
        for d in data:
            if d[0] == '0':
                with_mask += 1
            elif d[0] == '1':
                without_mask += 1
            else:
                mask_weared_incorrect += 1
        img_name = str(i) + '.png'
        ans.append([img_name, len(data), with_mask, without_mask, mask_weared_incorrect])

ans = pd.DataFrame(ans, columns=['图片名称', '人脸数量', '正确佩戴数量', '未佩戴数量', '未正确佩戴数量'], index=None)
ans.to_excel('赛题B提交结果.xlsx', index=None)