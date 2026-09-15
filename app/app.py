from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jenkins EKS Helm Project</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
                background-color: #f4f4f4;
            }

            .container {
                background: white;
                width: 600px;
                margin: auto;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
            }

            h1 {
                color: #333;
            }

            p {
                font-size: 18px;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🚀 Jenkins CI/CD Project</h1>

            <p>Application successfully deployed!</p>

            <p>
                Docker + Docker Hub + Jenkins + Helm + Amazon EKS
            </p>

            <p>
                Version: BUILD_VERSION
            </p>
        </div>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return {
        "status": "UP",
        "application": "jenkins-eks-helm-app"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
