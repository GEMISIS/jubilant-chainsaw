import cv2
# import pytesseract
from datetime import datetime
import pywintypes, win32file, win32con

# Updates the file on Windows only. Maybe will add updates in the future for other OS'.
def changeFileCreationTime(fname, date, time):
    newtime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    wintime = pywintypes.Time(newtime.timestamp())
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, wintime, wintime)

    winfile.close()

# Gets the video timestamp and use the appropriate time and date.
def getVideoTimestamp(fname):
    date = '2000-01-01'
    time = '00:00:00'

    # Get the video and find the frame with the necessary text.
    cap = cv2.VideoCapture(fname)
    while(cap.isOpened()):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)

        # Look for text here.
        # text = pytesseract.image_to_string(gray)
        # print(text)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return date, time

print('Converting...')

date, time = getVideoTimestamp('sample.mp4')
changeFileCreationTime('sample.mp4', date, time)

print('Done!')