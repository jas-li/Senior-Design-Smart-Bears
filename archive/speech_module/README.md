# Speech-To-Text Module

We are using OpenAI's Whisper, an OpenSource automatic speech recognition model. 

### Whisper.cpp

In a seperate folder outside of this repository, clone the [whisper.cpp repository](https://github.com/ggerganov/whisper.cpp).
```
git clone https://github.com/ggerganov/whisper.cpp.git
```

Navigate into the directory:
```
cd whisper.cpp
```

Then, download one of the Whisper models converted in ggml format. For example:
```
sh ./models/download-ggml-model.sh base.en
```

Now build the whisper-cli example:
```
# build the project
cmake -B build
cmake --build build --config Release
```

Install libraries:
```
# install SDL2
sudo apt-get install libsdl2-dev
```

Make the whisper-stream tool to capture audio from the microphone:
```
cmake -B build -DWHISPER_SDL2=ON
cmake --build build --config Release
```

### Editing stream.cpp

If you need to edit `examples/stream/stream.cpp`, you will need to rebuild whisper-stream:

```
cmake --build build --config Release
```

### Run Whisper.cpp Module

Finally, run this command:
```
./build/bin/whisper-stream
```