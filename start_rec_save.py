import streamlit as st
import pyaudio
import wave
import threading

# 전역 변수 설정
is_recording = False
frames = []

#녹음
def recording():
    global is_recording, frames
    is_recording = True
    frames = []

    # 오디오 설정
    chunk = 1024
    format = pyaudio.paInt16
    channels = 2
    rate = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    while is_recording:
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

#정지&저장
def stop_and_save_recording(filename):
    global is_recording
    is_recording = False
    if frames:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()
        st.success(f'Recording saved as {filename}')
    else:
        st.error('No recording to save.')
    st.audio(file_path, format='audio/wav')


def main() -> None:
    if 'audio_state' not in st.session_state:
        st.session_state['audio_state'] = '듣기'

    q_audio_path = 'test_q.wav'

    if st.button(st.session_state['audio_state']):
        play_audio(q_audio_path) # st.audio를 사용하여 오디오 파일 재생
        st.session_state['audio_state'] = '다시 듣기'


    if st.button("재생"):
        audio = threading.Thread(target=recording)
        audio.start()
        st.write('Recording started')

    if st.button('다음'):
        stop_and_save_recording('output.wav')




if __name__ == "__main__":
    main()
