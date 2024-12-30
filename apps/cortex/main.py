import uvicorn
import argparse

def run_app(port: int = 11168):
    from app.main import app as web_app
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True
    )

def run_api(port: int = 11169):
    from app.api import app as api_app
    uvicorn.run(
        "app.api:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True
    )

def main():
    parser = argparse.ArgumentParser(description="Run Cortex App or API")
    parser.add_argument(
        "mode", 
        choices=["app", "api", "both"], 
        help="Run the web app, API, or both"
    )
    parser.add_argument(
        "--app-port", 
        type=int, 
        default=11168, 
        help="Port for the web app (default: 11168)"
    )
    parser.add_argument(
        "--api-port", 
        type=int, 
        default=11169, 
        help="Port for the API (default: 11169)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "app":
        run_app(args.app_port)
    elif args.mode == "api":
        run_api(args.api_port)
    elif args.mode == "both":
        import multiprocessing
        
        app_process = multiprocessing.Process(
            target=run_app, 
            args=(args.app_port,)
        )
        api_process = multiprocessing.Process(
            target=run_api, 
            args=(args.api_port,)
        )
        
        app_process.start()
        api_process.start()
        
        app_process.join()
        api_process.join()

if __name__ == "__main__":
    main() 