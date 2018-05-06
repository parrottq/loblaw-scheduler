# Maintainer: Quinn Parrott <github@parrottq.ca>
pkgname=loblaw-scheduler-git
pkgver=r5.d22d075
pkgrel=1
pkgdesc="iCalendar adapter for Loblaw employee schedules"
arch=('any')
url="https://github.com/parrottq/loblaw-scheduler"
license=('MIT')
groups=()
depends=('python-requests' 'python-flask' 'python-icalendar' 'gunicorn')
makedepends=('git')
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")
replaces=()
backup=()
options=()
source=('git+https://github.com/parrottq/loblaw-scheduler' 'loblaw-scheduler.service')
noextract=()
md5sums=('SKIP'
         '821fe91817ac15fdc4f33d993b66f1d2')


pkgver() {
	cd "$srcdir/${pkgname%-git}"

	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
	cd "$srcdir/${pkgname%-git}"
	python setup.py build
}

package() {
	cd "$srcdir/${pkgname%-git}"
	install -Dm644 "$srcdir/loblaw-scheduler.service" "$pkgdir/usr/lib/systemd/system/loblaw-scheduler.service"
	python setup.py install --root="$pkgdir/" --optimize=1 --skip-build
}
