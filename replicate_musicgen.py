import replicate

def generate_music_replicate(duration, prompt="exciting basketball game"):
    output_url = replicate.run(
        "facebookresearch/musicgen:7a76a8258b23fae65c5a22debb8841d1d7e816b75c2f24218cd2bd8573787906",
        input={"model_version": "melody", "prompt": prompt, "duration": int(min(30, duration))},
    )
    print(output_url)
    
    return output_url