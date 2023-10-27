import os
import subprocess
import gradio as gr
import imageio_ffmpeg as ffmpeg

# execute a CLI command
def execute_command(command: str) -> None:
    subprocess.run(command, check=True)


def infer(video_source, audio_target):
    
    output = "results/result.mp4"
    command = [
      f"python", 
      f"inference.py",
      f"--face={video_source}",
      f"--audio={audio_target}",
      f"--outfile={output}"
    ]

    execute_command(command)

    input_file = output  # Replace with the path to your input video
    output_file = 'output_video.mp4'  # Replace with the desired output file path
    
    # Define the codec options for the output video (e.g., H.264 and AAC for MP4)
    codec_options = "-c:v libx264 -c:a aac"
    
    # Use ffmpeg to transcode the video
    command = f"ffmpeg -i {input_file} {codec_options} {output_file}"
    ffmpeg_cmd = ffmpeg.get_ffmpeg_exe()
    return_code = ffmpeg.cmd(command, ffmpeg_path=ffmpeg_cmd)
    
    if return_code == 0:
        print("Video conversion successful.")
    else:
        print("Video conversion failed.")

    return output_file

css="""
#col-container{
    margin: 0 auto;
    max-width: 720px;
    text-align: left;
}
"""
    
with gr.Blocks(css=css) as demo:
    with gr.Column(elem_id="col-container"):
        gr.HTML("""
        <h2 style="text-align: center;">Video ReTalking</h2>
        <p style="text-align: center;">
            Audio-based Lip Synchronization for Talking Head Video Editing in the Wild
        </p>
                """)
        video_source = gr.Video(label="Source Video", type="filepath")
        audio_target = gr.Audio(label="Audio Target", type="filepath")
        
        submit_btn = gr.Button("Submit")
        result = gr.Video(label="Result")

        gr.Examples(
          label="Examples",
          examples=[
            ["examples/face/1.mp4", "examples/audio/1.wav"]
          ],
          fn=infer,
          inputs=[video_source, audio_target],
          outputs=[result]
        )
    
    submit_btn.click(fn=infer, inputs=[video_source, audio_target], outputs=[result])
    
demo.queue(max_size=12).launch()
