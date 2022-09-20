run:
    python3 keycollator.py -l -v

setup: requirements.txt
    pip3 install -r requirements.txt

clean:
    rm -rf __pycache__

push:
    git add .
    git -m "Updated"
    git push

run_env:
    source venv/bin/activate

    
