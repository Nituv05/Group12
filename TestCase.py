import random

def generate_test_case():
    N = 900
    Q = random.randint(200,250)  # Q sẽ phụ thuộc vào N  
    
    pred = []
    for _ in range(Q):
        i = random.randint(1, N)
        j = random.randint(1, N)
        while i == j:  # Đảm bảo công việc i và j khác nhau
            j = random.randint(1, N)
        pred.append((i, j))
    
    # Sinh thời gian cho mỗi công việc
    d = [random.randint(10, 100) for _ in range(N)] 
    
    # Sinh số lượng đội ngũ và thời gian có sẵn của mỗi đội
    M = 400
    s = [random.randint(25, 200) for _ in range(M)]  # Thời gian bắt đầu của mỗi nhóm
    
    # Sinh số lượng chi phí (K)
    K = random.randint(300,400)  
    c = [[0 for _ in range(M + 1)] for _ in range(N + 1)]  # Khởi tạo ma trận chi phí
    
    # Đảm bảo đủ K chi phí
    cost_count = 0
    while cost_count < K:
        i = random.randint(1, N)
        j = random.randint(1, M)
        cost = random.randint(20, 100)  # Chi phí ngẫu nhiên
        if c[i][j] == 0:  # Chỉ thêm chi phí nếu chưa có
            c[i][j] = cost
            cost_count += 1
    
    # N và Q
    print(N, Q)
    # Các cặp thứ tự ưu tiên 
    for i, j in pred: 
        print(i, j)
    
    # Thời gian hoàn thành công việc
    print(' '.join(map(str, d)))
    
    # Số lượng nhóm M
    print(M)
    
    # Thời điểm bắt đầu của nhóm
    print(' '.join(map(str, s)))
    
    # Số lượng chi phí K
    print(K)
    
    # Các chi phí c(i,j)
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if c[i][j] > 0:  # Chỉ in các chi phí không phải là 0
                print(i, j, c[i][j])

# Chạy generator để tạo test case
if __name__ == "__main__":
    generate_test_case()
