FROM baneeishaque/gitpod-full-1366x768-tint2-pcmanfm-zsh-android-studio-gh-chrome-idea-pycharm-anaconda3-2020-11

RUN cd $HOME \
 && wget "https://raw.githubusercontent.com/Baneeishaque/Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting/main/environment.yml" \
 && conda env create -f environment.yml \
 && rm environment.yml

RUN pyenv global anaconda3-2020.11/envs/Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting
RUN echo "conda activate Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting" >> ~/.bashrc
RUN echo "conda activate Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting" >> ~/.zshrc
