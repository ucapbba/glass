import pytest

# check if fitsio is available for testing
try:
    import fitsio
except ImportError:
    HAVE_FITSIO = False
else:
    del fitsio
    HAVE_FITSIO = True

import glass.user as user
import numpy as np

@pytest.mark.skipif(not HAVE_FITSIO, reason="test requires fitsio")
def _test_append(fits, data, names):
    """Write routine for FITS data."""
    cat_name = 'CATALOG'
    if cat_name not in fits:
        fits.write_table(data, names=names, extname=cat_name)
    else:
        hdu = fits[cat_name]
        hdu.write(data, names=names, firstrow=hdu.get_nrows())


delta = 0.001  # Number of points in arrays
myMax = 1000  # Typically number of galaxies in loop
exceptInt = 750  # Where test exception occurs in loop
filename = "MyFile.Fits"


@pytest.mark.skipif(not HAVE_FITSIO, reason="test requires fitsio")
def test_basic_write(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    filename_gfits = "gfits.fits"  # what GLASS creates
    filename_tfits = "tfits.fits"  # file create on the fly to test against

    with user.write_context(d / filename_gfits, ext="CATALOG") as out, fitsio.FITS(d / filename_tfits, "rw", clobber=True) as myFits:
        for i in range(0, myMax):
            array = np.arange(i, i+1, delta)  # array of size 1/delta
            array2 = np.arange(i+1, i+2, delta)  # array of size 1/delta
            out.write(RA=array, RB=array2)
            arrays = [array, array2]
            names = ['RA', 'RB']
            _test_append(myFits, arrays, names)

    from astropy.io import fits
    with fits.open(d / filename_gfits) as g_fits, fits.open(d / filename_tfits) as t_fits:
        glass_data = g_fits[1].data
        test_data = t_fits[1].data
        assert glass_data['RA'].size == test_data['RA'].size
        assert glass_data['RB'].size == test_data['RA'].size


@pytest.mark.skipif(not HAVE_FITSIO, reason="test requires fitsio")
def test_write_exception(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()

    try:
        with user.write_context(d / filename, ext="CATALOG") as out:
            for i in range(0, myMax):
                if i == exceptInt:
                    raise Exception("Unhandled exception")
                array = np.arange(i, i+1, delta)  # array of size 1/delta
                array2 = np.arange(i+1, i+2, delta)  # array of size 1/delta
                out.write(RA=array, RB=array2)

    except Exception:
        from astropy.io import fits
        with fits.open(d / filename) as hdul:
            data = hdul[1].data
            assert data['RA'].size == exceptInt/delta
            assert data['RB'].size == exceptInt/delta

            fitsMat = data['RA'].reshape(exceptInt, int(1/delta))
            fitsMat2 = data['RB'].reshape(exceptInt, int(1/delta))
            for i in range(0, exceptInt):
                array = np.arange(i, i+1, delta)  # re-create array to compare to read data
                array2 = np.arange(i+1, i+2, delta)
                assert array.tolist() == fitsMat[i].tolist()
                assert array2.tolist() == fitsMat2[i].tolist()


@pytest.mark.skipif(not HAVE_FITSIO, reason="test requires fitsio")
def test_out_filename(tmp_path):

    fits = fitsio.FITS(filename, "rw", clobber=True)
    writer = user.FitsWriter(fits)
    assert writer.fits._filename == filename


@pytest.mark.skipif(not HAVE_FITSIO, reason="test requires fitsio")
def test_write_none(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    with user.write_context(d / filename, ext="CATALOG") as out:
        out.write()
    assert 1 == 1


@pytest.mark.skipif(not HAVE_FITSIO, reason="test requires fitsio")
def test_write_yield(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    with user.write_context(d / filename, ext="CATALOG") as out:
        assert type(out) is user.FitsWriter
