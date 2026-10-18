#!/usr/bin/env python3
"""
Download Planck PR4 CMB data via healpy/camb.
Power spectra, lensing, and component separation maps.
"""
import os
import logging
from pathlib import Path
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
EXTERNAL_DIR = BASE_DIR / "data" / "external"
RAW_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

try:
    import healpy as hp
    import camb
    from camb import model, initialpower
    import requests
    from tqdm import tqdm
except ImportError as e:
    logger.error(f"Missing dependencies: {e}")
    logger.error("Install with: pip install healpy camb requests tqdm --break-system-packages")
    exit(1)


def download_planck_power_spectra():
    """Download Planck PR4 power spectra from official archive."""
    logger.info("Downloading Planck PR4 power spectra...")
    
    # Planck PR4 power spectra URLs (from PLA)
    urls = {
        "TT": "https://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_PowerSpect_CMB-TT-full_R3.01",
        "TE": "https://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_PowerSpect_CMB-TE-full_R3.01",
        "EE": "https://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_PowerSpect_CMB-EE-full_R3.01",
        "lensing": "https://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_Lensing_PowerSpect_R3.01",
    }
    
    spectra_dir = RAW_DIR / "planck_pr4_spectra"
    spectra_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    for name, url in urls.items():
        local_path = spectra_dir / f"planck_pr4_{name}.txt"
        try:
            response = requests.get(url, timeout=120)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Downloaded {name} spectrum")
                downloaded += 1
            else:
                logger.warning(f"Failed to download {name}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Error downloading {name}: {e}")
    
    return downloaded


def generate_camb_power_spectra():
    """Generate theoretical CMB power spectra using CAMB."""
    logger.info("Generating CAMB power spectra...")
    
    # Planck 2018 cosmology
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, omk=0, tau=0.0544)
    pars.InitPower.set_params(As=2.100e-9, ns=0.9649, r=0)
    pars.set_for_lmax(2500, lens_potential_accuracy=1)
    pars.WantTensors = False
    
    results = camb.get_results(pars)
    powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
    
    # Save spectra
    spectra_dir = EXTERNAL_DIR / "camb_spectra"
    spectra_dir.mkdir(parents=True, exist_ok=True)
    
    for key, spec in powers.items():
        if key in ['total', 'unlensed_scalar', 'lensed_scalar', 'tensor']:
            np.savetxt(spectra_dir / f"camb_{key}.txt", spec)
            logger.info(f"Saved CAMB {key} spectrum: {spec.shape}")
    
    # Also save lensing potential
    cl_pp = results.get_lens_potential_cls(2500)
    np.savetxt(spectra_dir / "camb_lensing_potential.txt", cl_pp)
    
    # Generate spectra for multiple cosmologies (for Fisher matrix / parameter estimation)
    logger.info("Generating multi-cosmology spectra for Fisher analysis...")
    cosmologies = [
        {"name": "planck2018", "H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.9649, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.06},
        {"name": "planck2015", "H0": 67.74, "ombh2": 0.02230, "omch2": 0.1188, "ns": 0.9667, "As": 2.130e-9, "tau": 0.066, "mnu": 0.06},
        {"name": "wmap9", "H0": 70.0, "ombh2": 0.02264, "omch2": 0.1138, "ns": 0.972, "As": 2.41e-9, "tau": 0.089, "mnu": 0.06},
        {"name": "high_H0", "H0": 73.0, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.9649, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.06},
        {"name": "low_H0", "H0": 65.0, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.9649, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.06},
        {"name": "high_ns", "H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.98, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.06},
        {"name": "low_ns", "H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.95, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.06},
        {"name": "high_tau", "H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.9649, "As": 2.100e-9, "tau": 0.08, "mnu": 0.06},
        {"name": "massive_nu", "H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.9649, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.15},
        {"name": "massless_nu", "H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "ns": 0.9649, "As": 2.100e-9, "tau": 0.0544, "mnu": 0.0},
    ]
    
    multi_dir = EXTERNAL_DIR / "camb_multi_cosmology"
    multi_dir.mkdir(parents=True, exist_ok=True)
    
    for cosmo in cosmologies:
        pars = camb.CAMBparams()
        pars.set_cosmology(H0=cosmo["H0"], ombh2=cosmo["ombh2"], omch2=cosmo["omch2"], 
                          mnu=cosmo["mnu"], omk=0, tau=cosmo["tau"])
        pars.InitPower.set_params(As=cosmo["As"], ns=cosmo["ns"], r=0)
        pars.set_for_lmax(2500, lens_potential_accuracy=1)
        pars.WantTensors = False
        
        results = camb.get_results(pars)
        powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
        
        np.savez(
            multi_dir / f"camb_{cosmo['name']}.npz",
            ell=np.arange(2, 2501),
            TT=powers['total'][2:, 0],
            EE=powers['total'][2:, 1],
            TE=powers['total'][2:, 3],
            BB=powers['total'][2:, 2],
            PP=results.get_lens_potential_cls(2500)[2:],
            cosmology=cosmo
        )
    
    logger.info(f"Generated {len(cosmologies)} cosmology spectra")
    return True


def download_planck_lensing_map():
    """Download Planck lensing convergence map."""
    logger.info("Downloading Planck lensing map...")
    
    url = "https://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_Lensing_Map_Komatsu_R3.00"
    local_path = RAW_DIR / "planck_lensing_map.fits"
    
    try:
        response = requests.get(url, timeout=300, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(local_path, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, 
                         desc="lensing_map.fits") as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            logger.info(f"Downloaded lensing map: {local_path.stat().st_size / 1e6:.1f} MB")
            return True
        else:
            logger.warning(f"Failed to download lensing map: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"Error downloading lensing map: {e}")
    
    return False


def generate_planck_likelihood_data():
    """Generate Planck-like likelihood data using CAMB."""
    logger.info("Generating Planck-like likelihood data...")
    
    # Generate binned power spectra for likelihood
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, omk=0, tau=0.0544)
    pars.InitPower.set_params(As=2.100e-9, ns=0.9649, r=0)
    pars.set_for_lmax(2500, lens_potential_accuracy=1)
    
    results = camb.get_results(pars)
    
    # Get binned spectra (like Planck likelihood)
    ls = np.arange(2, 2501)
    cl_tt = results.get_cmb_power_spectra(pars)['total'][:, 0]  # TT
    cl_te = results.get_cmb_power_spectra(pars)['total'][:, 3]  # TE
    cl_ee = results.get_cmb_power_spectra(pars)['total'][:, 1]  # EE
    
    # Save as numpy arrays
    np.save(EXTERNAL_DIR / "planck_like_tt.npy", cl_tt[2:])
    np.save(EXTERNAL_DIR / "planck_like_te.npy", cl_te[2:])
    np.save(EXTERNAL_DIR / "planck_like_ee.npy", cl_ee[2:])
    np.save(EXTERNAL_DIR / "planck_like_ell.npy", ls)
    
    logger.info("Saved Planck-like binned spectra")
    return True


def main():
    logger.info("Starting Planck PR4 / CAMB data download...")
    
    total_size = 0
    
    # 1. Download official Planck power spectra
    download_planck_power_spectra()
    
    # 2. Generate CAMB theoretical spectra
    generate_camb_power_spectra()
    
    # 3. Generate Planck-like likelihood data
    generate_planck_likelihood_data()
    
    # 4. Try to download lensing map (large, may fail)
    download_planck_lensing_map()
    
    # Calculate total size
    for d in [RAW_DIR, EXTERNAL_DIR]:
        for f in d.rglob("*"):
            if f.is_file():
                total_size += f.stat().st_size
    
    logger.info(f"Planck/CAMB data complete. Total size: {total_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()