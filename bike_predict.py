import streamlit as st
import sys
import subprocess

st.set_page_config(
    page_title="Debug Mode",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 DEBUG MODE - Installed Packages")

st.subheader("📦 Installed Python Packages:")
try:
    import pkg_resources
    installed_packages = [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
    for pkg in sorted(installed_packages):
        if any(x in pkg.lower() for x in ['sklearn', 'scikit', 'xgboost', 'pandas', 'numpy']):
            st.write(f"✅ {pkg}")
        else:
            st.write(f"   {pkg}")
except Exception as e:
    st.error(f"Error listing packages: {e}")

st.divider()

st.subheader("📁 Files in current directory:")
import os
files = os.listdir('.')
for f in files:
    if f.endswith('.txt') or f.endswith('.sav') or f.endswith('.py'):
        st.write(f"- {f}")

st.divider()

st.subheader("📄 Requirements.txt content:")
if 'requirements.txt' in files:
    with open('requirements.txt', 'r') as f:
        st.code(f.read())
else:
    st.error("requirements.txt NOT FOUND!")

st.divider()

st.subheader("🔄 Attempting to install scikit-learn...")
if st.button("Install scikit-learn now"):
    result = subprocess.run([sys.executable, "-m", "pip", "install", "scikit-learn==1.2.2"], 
                          capture_output=True, text=True)
    st.text("Output:")
    st.code(result.stdout)
    if result.stderr:
        st.error("Error:")
        st.code(result.stderr)
    st.success("Installation attempt complete. Please reboot the app.")
