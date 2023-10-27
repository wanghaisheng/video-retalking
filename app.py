import os
import subprocess
import gradio as gr

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

    return output

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
            
        </p>
                """)
        video_source = gr.Video(label="Source Video", type="filepath")
        audio_target = gr.Audio(label="Audio Target", type="filepath")
        
        submit_btn = gr.Button("Submit")
        result = gr.Video(label="Result")
    
    submit_btn.click(fn=infer, inputs=[video_source, audio_target], outputs=[result])
    gr.Examples(
      label="Examples",
      examples=[
        ["examples/face/1.mp4", "examples/audio/1.wav"]
      ],
      fn=infer,
      inputs=[video_source, audio_target],
      outputs=[result]
    )
demo.queue(max_size=12).launch()
