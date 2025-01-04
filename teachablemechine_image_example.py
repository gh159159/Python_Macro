import tensorflow.keras
import numpy as np
import cv2

# 모델 위치
model_filename = 'keras_model.h5'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

# 이미지 처리하기
def preprocessing(image_path):
    # 이미지를 파일에서 읽기
    frame = cv2.imread(image_path)

    # 사이즈 조정 (티쳐블 머신에서 사용한 이미지 사이즈로 변경)
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

image0 = cv2.imread("0.jpg")
image1 = cv2.imread("1.jpg")
image2 = cv2.imread("2.jpg")

# 사용자에게 이미지 파일 경로 입력 받기
# image_path = input("예측할 이미지 파일의 경로를 입력하세요: ")
image_path = "다운로드.jpg"
preprocessed = preprocessing(image_path)
prediction = predict(preprocessed)
print("예측비율", prediction)
prediction_c = np.argmax(prediction)
print("예측분류", prediction_c)

# 예측 결과에 따라 이미지를 화면에 표시
if prediction_c == 0:
    print('CLEAR')
    cv2.imshow("Prediction Result", image0)
    cv2.putText(image0, 'CLEAR', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
elif prediction_c == 1:
    print('RED PEN')
    cv2.imshow("Prediction Result", image1)
    cv2.putText(image1, 'RED PEN', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
elif prediction_c == 2:
    print('BLACK PEN')
    cv2.imshow("Prediction Result", image2)
    cv2.putText(image2, 'BLACK PEN', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

cv2.waitKey(0)
cv2.destroyAllWindows()
