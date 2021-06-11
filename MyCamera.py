import cv2
import SendFile

# Capture video
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")

# Saving video
output = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
i = 0

# Procceding after checking if camera is opened or not
while (cap.isOpened()):
    ret, prev_frame = cap.read()
    ret, next_frame = cap.read()
    if ret == True:
        print(cap.get(cv2.CAP_PROP_FRAME_WIDTH),
              cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Taking difference between frames so that movement is detected
        difference = cv2.absdiff(prev_frame, next_frame)
        gray = cv2.cvtColor(difference, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, 3)

# Making border around moving object using contours and saving images
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(prev_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imwrite("Capture"+str(i)+".jpg", prev_frame)
            i += 1
        output.write(prev_frame)
        cv2.imshow("Recorder...", prev_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
output.release()
cv2.destroyAllWindows()
email = SendFile.sendEmail()
