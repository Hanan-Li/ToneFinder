import matchering as mg

# Let's keep info and warning outputs here, muting out the debug ones
mg.log(info_handler=print, warning_handler=print)

mg.process(
    target="audio_files/251.wav",
    reference="audio_files/fender_251.wav",
    # pcm16 and pcm24 are just basic shortcuts
    # You can also use the Result class to make some advanced results
    results=[
        # Basic WAV 16-bit, match + master
        mg.pcm16("my_song_master_16bit.wav"),
        # FLAC 24-bit, match only (no limiter), normalized to -0.01 dB
        # Recommendations for adjusting the amplitude will be displayed in the debug print if it is enabled
        mg.Result(
            "custom_result_24bit_no_limiter.wav", subtype="PCM_24", use_limiter=False
        ),
        # AIFF 32-bit float, match only (no limiter), non-normalized
        # Can exceed 0 dB without clipping
        # So you can directly feed it to some VST limiter in your DAW

        # More available formats and subtypes:
        # https://pysoundfile.readthedocs.io/en/latest/#soundfile.available_formats
        # https://pysoundfile.readthedocs.io/en/latest/#soundfile.available_subtypes
    ],
    ir_file = "mid_ir.wav"
)