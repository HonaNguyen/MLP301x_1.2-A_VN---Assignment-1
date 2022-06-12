import os
# Import 2 thư viện numpy và panda
import pandas as pd


# Hàm kiểm tra id học sinh có thỏa mãn id có độ dài 9, bắt đầu bằng kí tự N
# Và đằng sau ký tự N là 8 chữ số trong khoảng [0,9]
def checkId(id) -> bool:
    if len(id) != 9:
        return False
    return all('0' <= x <= '9' for x in id[1:]) and (id[0] == 'N')

if __name__ == "__main__":

    # Task 1:
    # Chương trình cho phép người dùng nhập tên của file và truy cập vào
    # Đảm bảo file và dữ liệu nằm cùng folder

    while True:
        try:
            filename = input("Please enter a file you want to access: ")
            filename = str(filename) + str(".txt")

            # Lấy đường dẫn hiện tại
            path = os.getcwd()
            path += "\\" + filename

            with open(path, mode="r", encoding="utf-8") as file:
                data_from_file = file.readlines()

            print("Open {} successfully !!!\n".format(filename))
            break
        except:
            print("Sorry! File Not Found. Please enter another name !\n")

    
    # Task 2: Kiểm tra dữ liệu
    # Kiểm tra dữ liệu
    print(10*"*" + "Checking Data" + 10*"*")

    # List để lưu các dòng dữ liệu hợp lệ và không hợp lệ
    valid_data = []
    invalid_data = []
    for data in data_from_file:
        tmp_data = data.replace("\n", "").split(",")
        if len(tmp_data) != 26 or (checkId(tmp_data[0]) is False):
            invalid_data.append(tmp_data)
        else:
            valid_data.append(tmp_data)

    if len(invalid_data) == 0:
        print("No Error Found !")
    else:
        for x in invalid_data:
            if len(x) != 26:
                print("Invalid line of data: does not contain exactly 26 values:")
                print(",".join(str(y) for y in x))
                print()
            else:
                print("Invalid line of data: N# is invalid")
                print(",".join(str(y) for y in x))
                print()
    
    print()
    print(10*"*" + "REPORT" + 10*"*" + "\n")
    print("Total valid lines of data: ",len(valid_data))
    print("Total invalid line of data: ",len(invalid_data))

    # Task 3: Chấm điểm
    # Đúng: +4
    # Sai: -1
    # Bỏ qua: 0
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    answer_key = answer_key.split(",")

    # Tạo list chứa số điểm cho mỗi câu trả lời tương ứng với mỗi học sinh
    valid_points = []
    for i in range(len(valid_data)):
        tmp = []
        tmp.append(valid_data[i][0])
        for j in range(1, len(valid_data[i])):
            if valid_data[i][j] == '':
                tmp.append(0)
            elif valid_data[i][j] != answer_key[j-1]:
                tmp.append(-1)
            else:
                tmp.append(4)
        valid_points.append(tmp)

    # Tạo list chứa các tên cột (đặc tính) trong data frame
    # Cột bao gồm ID và 25 đáp án
    columns = []
    columns.append("ID")
    for x in range(1, 26): 
        columns.append(x)

    # Tạo data frame
    df = pd.DataFrame.from_records(valid_points, columns=columns)

    # Thêm cột Total points lưu trữ tổng số điểm của mỗi học sinh
    df["Total_points"] = df[columns[1:]].sum(axis=1)
    
    print("Mean (average) score: ", df["Total_points"].mean())
    print("Highest score: ", df["Total_points"].max())
    print("Lowest score: ", df["Total_points"].min())
    print("Range of scores: ", df["Total_points"].max() - df["Total_points"].min())
    print("Median score: ",df["Total_points"].median())


    # Task 4: Xuất điểm của từng học sinh ra file
    filename = filename.replace(".txt", "_grades.txt")
    # Lấy đường dẫn hiện tại
    path = os.getcwd()
    path += "\\" + filename
    if not os.path.exists(path):
        with open(path, mode="w", encoding="utf-8") as file:
            file.write("")
            file.truncate()
    
    # Ghi ra file
    df[["ID", "Total_points"]].to_csv(path, header=None, index=None)
    
    