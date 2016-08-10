FROM itamtao/python-basis

MAINTAINER Tao Lin <itamtao@gmail.com>

# install numpy
RUN pip install --no-cache-dir numpy

# install scipy, matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatlas-base-dev \
    gfortran \
    && apt-get clean \
    && pip install --no-cache-dir scipy

# install matplotlib
RUN pip install --no-cache-dir matplotlib

# install scikit-learn
RUN pip install --no-cache-dir scikit-learn

# install ipython
RUN pip install --no-cache-dir ipython

# install joblib
RUN pip install --no-cache-dir joblib

# install pandas
RUN pip install --no-cache-dir pandas

# install cython
RUN pip install --no-cache-dir cython


USER tlin
VOLUME /home/tlin/notebooks
VOLUME /nltk
WORKDIR /home/tlin/notebooks

RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh \
      && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
