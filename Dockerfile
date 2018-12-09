FROM python:3.7

ENV INSTALL_DIRECTORY="/ip-communicator"
ENV PYTHONPATH="${INSTALL_DIRECTORY}"

ADD requirements.txt "${INSTALL_DIRECTORY}/requirements.txt"
RUN pip --disable-pip-version-check install -U -r "${INSTALL_DIRECTORY}/requirements.txt"

ADD . "${INSTALL_DIRECTORY}"
WORKDIR "${INSTALL_DIRECTORY}"

ENTRYPOINT ["python", "ipcommunicator/cli.py"]

CMD ["--help"]
