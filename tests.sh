#!/bin/bash

export DJANGO_SETTINGS_MODULE="test.djangoproject.settings"

echo ""
echo "==============================================================================="
echo "Test with Python 3.2 support"
rm -rf Test
cat << EOF | python2.7 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
3.2
0.1
yes
yes
no
EOF
cd Test
python3.2 setup.py build_ext > /dev/null
python3.2 setup.py doctest > /dev/null
python3.2 setup.py test > /dev/null
cd ..

echo ""
echo "==============================================================================="
echo "Test with Python 2.7, 3.2 (via six) support"
rm -rf Test
cat << EOF | python2.7 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
2.7
yes
0.1
no
no
no
EOF
cd Test
python2.7 setup.py build_ext > /dev/null
python2.7 setup.py doctest > /dev/null
python2.7 setup.py test > /dev/null
python3.2 setup.py build_ext > /dev/null
python3.2 setup.py doctest > /dev/null
python3.2 setup.py test > /dev/null
cd ..

echo ""
echo "==============================================================================="
echo "Test with Python 2.6, 2.7, 3.2 (via six) support"
rm -rf Test
cat << EOF | python2.7 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
2.6
yes
0.1
no
no
no
EOF
cd Test
python2.6 setup.py build_ext > /dev/null
python2.6 setup.py doctest > /dev/null
python2.6 setup.py test > /dev/null
python2.7 setup.py build_ext > /dev/null
python2.7 setup.py doctest > /dev/null
python2.7 setup.py test > /dev/null
python3.2 setup.py build_ext > /dev/null
python3.2 setup.py doctest > /dev/null
python3.2 setup.py test > /dev/null
cd ..

echo ""
echo "==============================================================================="
echo "Test with Python 2.6 & 2.7 support"
rm -rf Test
cat << EOF | python2.7 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
2.6
no
no
0.1
no
no
no
EOF
cd Test
python2.6 setup.py build_ext > /dev/null
python2.6 setup.py doctest > /dev/null
python2.6 setup.py test > /dev/null
python2.7 setup.py build_ext > /dev/null
python2.7 setup.py doctest > /dev/null
python2.7 setup.py test > /dev/null
cd ..


echo ""
echo "==============================================================================="
echo "Test with Django and Tastypie, Python 2.7 only"
rm -rf Test
cat << EOF | python2.7 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
2.7
yes
0.1
yes
yes
yes
yes
yes
yes
EOF
cd Test
python2.7 setup.py build_ext > /dev/null
python2.7 setup.py doctest > /dev/null
python2.7 setup.py test > /dev/null
cd ..

echo ""
echo "==============================================================================="
echo "Test runtime with python 2.6"
rm -rf Test
cat << EOF | python2.6 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
3.2
0.1
yes
yes
no
EOF

echo ""
echo "==============================================================================="
echo "Test runtime with python 2.7"
rm -rf Test
cat << EOF | python2.7 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
3.2
0.1
yes
yes
no
EOF
cd Test
python3.2 setup.py build_ext > /dev/null
python3.2 setup.py doctest > /dev/null
python3.2 setup.py test > /dev/null
cd ..


echo ""
echo "==============================================================================="
echo "Test runtime with python 3.2"
rm -rf Test
cat << EOF | python3.2 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
3.2
0.1
yes
yes
no
EOF
cd Test
python3.2 setup.py build_ext > /dev/null
python3.2 setup.py doctest > /dev/null
python3.2 setup.py test > /dev/null
cd ..

echo ""
echo "==============================================================================="
echo "Test runtime with python 3.2"
rm -rf Test
cat << EOF | python3.2 -c 'from starterpyth.core import main; main()'
Test
test
19pouces.net
d9pouces
d9pouces@19pouces.net
cecill b
2.6
yes
0.1
yes
no
no
no
EOF
cd Test
python2.6 setup.py build_ext > /dev/null
python2.6 setup.py doctest > /dev/null
python2.6 setup.py test > /dev/null
python3.2 setup.py build_ext > /dev/null
python3.2 setup.py doctest > /dev/null
python3.2 setup.py test > /dev/null
cd ..
