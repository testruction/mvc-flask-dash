FROM docker.io/amd64/python:3.10 as builder

COPY ./src /usr/local/src/app/src
COPY ./MANIFEST.in /usr/local/src/app/
COPY ./pyproject.toml /usr/local/src/app/
COPY ./README.md /usr/local/src/app/
COPY ./setup.cfg /usr/local/src/app/
COPY ./VERSION /usr/local/src/app/

ARG ADDITIONAL_PIP_PACKAGES
RUN python3 -m pip install --upgrade pip \
    && pip3 --no-cache-dir install \
        'build' \
        'cryptography' \
        'gunicorn' \
        ${ADDITIONAL_PIP_PACKAGES} \
    && cd /usr/local/src/app/ \
    && python3 -m build

FROM docker.io/amd64/python:3.10-slim

ARG IMAGE_VERSION

LABEL vendor='Testruction.io' \
      io.testruction.version="${IMAGE_VERSION}" \
	  io.testruction.related-product='mvc-flask-dash' \
	  io.testruction.description='MVC based Flask application including Dash components' \
      io.testruction.team="Testructers"

COPY --from=builder /usr/local/src/app/dist/*.tar.gz /tmp/

# Create the internal user
ENV OCI_USER_ID='10001' \
    OCI_USER='sysops'

RUN groupadd --gid "${OCI_USER_ID}" "${OCI_USER}" \
    && useradd --system --uid "${OCI_USER_ID}" --gid "${OCI_USER}" "${OCI_USER}" \
    && python3 -m pip install --upgrade pip \
    && pip3 --no-cache-dir install $(ls /tmp/*.tar.gz)

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && mkdir -vp /entrypoint.d/ \
    && chmod -R +x /entrypoint.d/

ENTRYPOINT [ "/entrypoint.sh" ]

# Activation de l'utilisateur intégré
USER ${OCI_USER}
WORKDIR ${HOME}/
COPY ./src/wsgi.py ${HOME}/wsgi.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
