from flask import Flask, render_template, Response
import cv2
import argparse
import akhdefo_functions

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process command line arguments')
parser.add_argument('--hls_url', default=None,
                    help='HLS URL or 0 for PC webcam or path to a video file')
parser.add_argument('--port', type=int, default=80,
                    help='Port number')
parser.add_argument('--alpha', type=float, default=0.5,
                    help='Alpha value')
parser.add_argument('--save_output', type=bool, default=False,
                    help='Save output')
parser.add_argument('--output_filename', default='example.mp4',
                    help='Output filename')
parser.add_argument('--ssim_threshold', type=float, default=0.75,
                    help='SSIM threshold')
parser.add_argument('--pyr_scale', type=float, default=0.5,
                    help='Pyr scale')
parser.add_argument('--levels', type=int, default=100,
                    help='Levels')
parser.add_argument('--winsize', type=int, default=120,
                    help='Win size')
parser.add_argument('--iterations', type=int, default=15,
                    help='Iterations')
parser.add_argument('--poly_n', type=int, default=7,
                    help='Poly N')
parser.add_argument('--poly_sigma', type=float, default=1.5,
                    help='Poly Sigma')
parser.add_argument('--flags', type=int, default=1,
                    help='Flags')
parser.add_argument('--show_video', type=bool, default=False,
                    help='Show video')
parser.add_argument('--streamer_option', default='mag',
                    help='Streamer option')

args = parser.parse_args()

# Ensure that the custom module is properly imported
try:
    from akhdefo_functions import measure_displacement_from_camera
except ImportError as e:
    print(f"Error importing 'akhdefo_functions': {e}")

app = Flask(__name__)

def generate_frames1():
    frames = measure_displacement_from_camera(
                hls_url=args.hls_url,
                alpha=args.alpha,
                save_output=args.save_output,
                output_filename=args.output_filename,
                ssim_threshold=args.ssim_threshold,
                pyr_scale=args.pyr_scale,
                levels=args.levels,
                winsize=args.winsize,
                iterations=args.iterations,
                poly_n=args.poly_n,
                poly_sigma=args.poly_sigma,
                flags=args.flags,
                show_video=args.show_video,
                streamer_option=args.streamer_option
            )

    for frame, g in frames:
        if frame is None or g is None:
            print("Error: Could not retrieve frame or g.")
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames2():
    frames = measure_displacement_from_camera(
                hls_url=args.hls_url,
                alpha=0.1,  # This alpha value is different than in generate_frames1
                save_output=args.save_output,
                output_filename=args.output_filename,
                ssim_threshold=0.8,  # This ssim_threshold value is different than in generate_frames1
                pyr_scale=args.pyr_scale,
                levels=args.levels,
                winsize=args.winsize,
                iterations=args.iterations,
                poly_n=args.poly_n,
                poly_sigma=args.poly_sigma,
                flags=args.flags,
                show_video=args.show_video,
                streamer_option=args.streamer_option
            )

    for frame, g in frames:
        if frame is None or g is None:
            print("Error: Could not retrieve frame or g.")
            continue
        ret, buffer = cv2.imencode('.jpg', g)
        g = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + g + b'\r\n')

@app.route('/video1')
def video1():
    return Response(generate_frames1(), content_type='multipart/x-mixed-replace; boundary=frame')

@app.route('/video2')
def video2():
    return Response(generate_frames2(), content_type='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=args.port, debug=True)
