#bài toán sẽ đọc video từ camera, sau đó hiện những hình ảnh theo dải màu
#cách chạy: mở anaconda, mở tiếp cửa sổ commandline, sau đó: CD tới thư mục chứa code này, chạy lệnh python color-range.py
# hoặc cũng có thể chạy bằng: python "tên đương dẫn\tên file python.py" 

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

list_hsv = []
h,v,s = 0,0,0
current_frame_hsv = None
points = []
#khi user nhấn chuột thì hàm này sẽ được gọi, đăng kí sự kiện bên dưới
def pick_color(event, x, y, flags, param):
    #phạm vi hàm: là global cho 3 biến h,v,s
    #global là keywork để muốn gán lại biến bên ngoài hàm, còn nếu đọc thì không cần
    global h,v,s
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = current_frame_hsv[y,x]
        h, s, v = pixel[0], pixel[1], pixel[2]
        print(h,s,v)

#lặp liên tục để xử lý
while(1):

    #đọc camera theo từng frame, frame là mảng matrix 3 chiều h x w x 3 (3 kênh màu BGR) - giống như file hình ảnh
    _, frame = cap.read()

    #do dùng kênh màu HSV hỗ trợ filter màu tốt hơn, nên chuyển về kênh HSV
    current_frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_range = np.array([h-15, s-45, v-45])
    upper_range = np.array([h+15, s+45, v+45])

    #hàm này sẽ loop qua điểm anh, nếu nó trong khoảng màu thì trả về, lưu ý giá trị là trả về bit.
    #Trong oopencv nhị phân là ảnh có hỗ trợ 2 loại: 0,1 hoặc 0,255 hai loại này đều chấp nhận
    mask = cv2.inRange(current_frame_hsv, lower_range, upper_range)

    #giờ đã có mask rồi thì thích làm gì cũng được
    #res = cv2.bitwise_and(frame,frame, mask= mask)

    #hàm này tạo 1 của sổ window có tên vẽ lên ngoài màn hinh
    cv2.imshow('Original-bat-ki-ten-gi',frame)

    #khai báo sự kiện khi nhấn chuột lên màn hình trên thì sẽ gọi hàm pick_color
    cv2.setMouseCallback('Original-bat-ki-ten-gi', pick_color)

    #thích show bao nhiêu màn hình cũng được
    cv2.imshow('Mask', mask)

    #sự kiện này để nhấn phím, nếu nhấn phím ESC (code = 27) thì sẽ dừng vòng lặp
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

#chỉ áp dụng những kiến thức viết bằng opencv, k dùng thư viện nhận dạng. sau này sẽ học sau.
#làm theo thứ tự bài nào cũng được

#bài tập 1: (bài này thì k liên quan đến opencv nhiều, liên quan đến cấu trúc dữ liệu + giải thuật)
#hiện giờ mới chỉ tạo được 1 mặt nạ bằng 1 dải màu, giờ làm nâng cao lên n dải màu: ví dụ được chọn xanh đỏ tím vàng...
#cách làm: lưu 1 list chứa các h,v,s sau mỗi lần click chuột sau đó dùng bitwise_or để gộp mặt nạ

#bài tập 2: (liên quan đến toán học: có 3 điểm thì có thể xác định góc)
#đo góc giữa hai đường thằng: nhấn chuột vào 3 điểm trên màn hình, rồi in góc của 3 điểm đó
#step: 1) x,y, nếu nhấn lần 1 thì vẽ cái hình tròn ở điểm nhấn chuột, đưa vào list, vẽ ra ngoài màn hình cv2.line( nếu đủ điều kiện là đường thẳng.. 3) tính góc, 4) cv2.putText

#bài tập 3: tự làm hình chữ nhật hay tròn màu gì đó để nhận dạng, vẽ viền - in ra tọa độ x,y lên màn hình,
# nếu di chuyển chữ nhật sang bên trái thì in ra chữ: bên trái, nếu bên phải in ra chữ bên phải,
# tính khoảng cách từ hình đó (trong phạm vi 30cm-100cm chẳng hạn)
#bài này sau này để làm xe tự chạy theo quả bóng màu:  khi lăn quả bóng, xe tự xác định hướng bóng lăn, kích cỡ quả bóng, để xe lùi hoặc tiến
#hành động bầy giờ  in chữ trái, phải lên màn hình, thì đó là để sau này mình sẽ biến nó thành tín hiệu để truyền xuống động cơ xe.
#các bước:
#1: Lọc màu bóng
#2: xác định contour hình tròn, khó quá, vuông
#3: tự nghĩ khi nào bên trái, khi nào bên phải
#ví dụ: https://www.youtube.com/watch?v=G4R9qPCT4Ho