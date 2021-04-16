FROM baneeishaque/gitpod-full-tint2-pcmanfm-zsh-as-gh-chrome-idea-pycharm-anaconda3-2020-11-as-canary-1366x625

RUN conda config --add channels intel

RUN cd $HOME \
 && wget "https://raw.githubusercontent.com/Baneeishaque/Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting/main/environment.yml" \
 && conda env create -f environment.yml \
 && rm environment.yml

RUN pyenv global anaconda3-2020.11/envs/Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting
RUN echo "conda activate Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting" >> ~/.bashrc
RUN echo "conda activate Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting" >> ~/.zshrc
