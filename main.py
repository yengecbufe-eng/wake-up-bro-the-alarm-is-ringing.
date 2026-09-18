import os
import time
import cv2
import mediapipe as mp

# Yerel video dosyanın adı
video_filename = 'uyan yeğen (ramiz dayı alarm).mp4'

if not os.path.exists(video_filename):
  print(
      f'HATA: "{video_filename}" dosyası klasörde bulunamadı! Lütfen videoyu'
      ' bu isimle klasöre koy.'
  )
  exit()

# MediaPipe yüz örgü (Face Mesh) modelini başlat
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

# Göz kapaklarının dikey mesafe indisleri (sol ve sağ göz üst/alt sınırları)
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374


def get_eye_opening(landmarks, top, bottom, w, h):
  top_p = landmarks[top]
  bot_p = landmarks[bottom]
  return abs((top_p.y - bot_p.y) * h)


cap = cv2.VideoCapture(0)

closed_start_time = None
required_duration = 5.0  # 5 saniye
video_played = False

print(
    'Kamera açılıyor... Gözlerini kapat ve 5 saniye boyunca kapalı tutarak bekle!'
)

while cap.isOpened():
  success, frame = cap.read()
  if not success:
    print('Kamera okunamadı.')
    break

  frame = cv2.flip(frame, 1)
  h, w, _ = frame.shape
  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  results = face_mesh.process(rgb_frame)
  eyes_closed = False

  if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
      landmarks = face_landmarks.landmark

      # Sol ve sağ göz açıklık mesafelerini hesapla
      left_dist = get_eye_opening(
          landmarks, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, w, h
      )
      right_dist = get_eye_opening(
          landmarks, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, w, h
      )

      # Göz açıklık eşik değeri (Bu mesafenin altına düşerse göz kapalı sayılır)
      threshold = 5.5

      if left_dist < threshold and right_dist < threshold:
        eyes_closed = True

  if eyes_closed:
    if closed_start_time is None:
      closed_start_time = time.time()
    else:
      elapsed = time.time() - closed_start_time
      remaining = max(0, int(required_duration - elapsed))
      cv2.putText(
          frame,
          f'Gozler Kapali! Kalan: {remaining}s',
          (30, 50),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.8,
          (0, 0, 255),
          2,
      )

      if elapsed >= required_duration and not video_played:
        print('5 saniye boyunca gözler kapalı kaldı! Video açılıyor...')
        video_played = True
        break
  else:
    closed_start_time = None
    cv2.putText(
          frame,
          'Gozlerini Kapat!',
          (30, 50),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.8,
          (0, 255, 0),
          2,
      )

  cv2.imshow('Goz Takibi - Cikis icin q', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

# Gözler 5 saniye kapalı kaldıysa videoyu sesli ve tam ekran başlat
if video_played:
  os.startfile(video_filename)
