FROM baneeishaque/gp-vnc-pcman-zsh-as-gh-chrome-idea-pycharm-conda3-hb-scrcpy-r-lfs-zilla-gram-matlab-mysql-phpstorm

RUN cd $HOME \
 && wget "https://raw.githubusercontent.com/Baneeishaque/Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting/main/environment.yml" \
 && conda env create -f environment.yml \
 && rm environment.yml

RUN pyenv global anaconda3-2020.11/envs/Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting
RUN echo "conda activate Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting" >> ~/.bashrc
RUN echo "conda activate Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpainting" >> ~/.zshrc
