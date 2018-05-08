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
source=('git+https://github.com/parrottq/loblaw-scheduler' 'loblaw-scheduler.service' 'sysusers.conf')
noextract=()
md5sums=('SKIP'
         '3a8ea2448edf445442b79d4ee4fd264b'
         '803813bdd85e655ccdb4078296d7f0ec')


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
	install -Dm644 "$srcdir/sysusers.conf" "$pkgdir/usr/lib/sysusers.d/loblaw-scheduler.conf"
	python setup.py install --root="$pkgdir/" --optimize=1 --skip-build
}
