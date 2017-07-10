FROM %%BASE_IMAGE%%

ENV LANG C.UTF-8

# Setup
RUN apk add --no-cache python3 \
    && pip3 install --no-cache --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy data for add-on
COPY button.py /
COPY find_button.py /etc/

CMD ["python3", "button.py"]