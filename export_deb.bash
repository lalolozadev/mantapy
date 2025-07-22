fpm -s dir -t deb -n mantapy -v 1.0 \
  --description "Mantapy: About Mantapy is a lightweight and intuitive Python tool designed for fast and clean data visualization." \
  --maintainer "Eduardo Loza @lalolozadev" \
  --url "https://github.com/lalolozadev/mantapy" \
  --license "MIT" \
  --category utils \
  --deb-user root \
  --deb-group root \
  --deb-priority optional \
  --deb-changelog changelog \
  --depends python3 \
  -C package_root \
  .
