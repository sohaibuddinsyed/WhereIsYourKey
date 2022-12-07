from flask import Flask, render_template, redirect, url_for, request, send_file
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256

import rsa
import requests
import datetime
import json
import binascii

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

UserIdKeyToUserName = {}
UserNameToUserKeyIds = {}
UserKeyIDs = {}
Credentials = {}

UserNames = {}
SignedInUser = None
SignedInKeyId = None
UserNameServerKeys = {}

UserObj = {}
BackUpKeys = {}

@app.route("/")
def hello():
    return redirect(url_for("about", userIdentity=""))


@app.route("/about/<userIdentity>", methods=["GET", "POST"])
def about(userIdentity):
    print("signed in user in about ->" + str(SignedInUser))
    if SignedInUser == None:
        return redirect(url_for("signup"))
    print("About section -" + str(SignedInUser))
    return render_template("about.html", userId=userIdentity)


@app.route("/keys/", methods=["GET", "POST"])
def keys():
    if SignedInUser == None:
        return redirect(url_for("signup"))
    if request.method == "POST":
        KeyId = request.form["keyId"]
        Domain = request.form["domain"]
        ServerKey = UserNameServerKeys[(UserNameToUserKeyIds[SignedInUser], Domain)]
        print(ServerKey)
        BackUpKey = BackUpKeys[SignedInUser]
        print(BackUpKey)
        body = {"userKeyStatus": False, "backupKeyStatus": True}

        message = json.dumps(body).encode()
        privateKey = RSA.import_key(ServerKey)
        signer = PKCS115_SigScheme(privateKey)
        signature = signer.sign(SHA256.new(message))
        print("Signature-gen:", binascii.hexlify(signature).decode())

        # hash = rsa.compute_hash(message, "SHA-256")
        # SK = rsa.PrivateKey.load_pkcs1(ServerKey.encode())
        # signature = rsa.sign_hash(hash, SK, "SHA-256")
        data = {"data": body, "signature": binascii.hexlify(signature).decode()}
        print(ServerKey)

        ## Post to the website backup public key
        url = "http://" + Domain + "/credential/" + KeyId + "/disable"
        res = requests.post(url, json.dumps(data))
        print(res)

        if res.status_code != 200:
            return render_template(
                "comments.html",
                keys=UserKeyIDs[SignedInUser],
                SignedInUser=SignedInUser,
                error=f"Failed to disable key {UserKeyIDs[SignedInUser][0]}",
            )

        for t in UserKeyIDs[SignedInUser]:
            if t[0] == KeyId:
                UserKeyIDs[SignedInUser].remove(t)
                UserKeyIDs[SignedInUser].append((t[0], t[1], False))
            return render_template(
                "comments.html", keys=UserKeyIDs[SignedInUser], SignedInUser=SignedInUser
            )

    if UserKeyIDs[SignedInUser] == []:
        print("Currentuser has no keys")
        CurrentUserKeys = []
    else:
        CurrentUserKeys = UserKeyIDs[SignedInUser]
        print(CurrentUserKeys)

    dictToSend = {"question": "what is the answer?"}
    return render_template("comments.html", keys=CurrentUserKeys, SignedInUser=SignedInUser)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        if (
            request.form["username"] == ""
            or request.form["password"] == ""
            or request.form["KeyUserID"] == ""
        ):
            error = "Invalid Credentials. Please try again."
        else:
            Credentials[request.form["username"]] = request.form["password"]
            UserIdKeyToUserName[request.form["KeyUserID"]] = request.form["username"]
            UserNameToUserKeyIds[request.form["username"]] = request.form["KeyUserID"]
            UserKeyIDs[request.form["username"]] = []

            publicKey, privateKey = rsa.newkeys(512)
            f = open("backUpKey.pem", "w")
            privateKeyPkcs1PEM = privateKey.save_pkcs1().decode()
            publicKeyPkcs1PEM = publicKey.save_pkcs1().decode()
            # publicKeyReloaded = rsa.PublicKey.load_pkcs1(publicKeyPkcs1PEM.encode('utf8'))
            f.write(privateKeyPkcs1PEM)
            f.close()

            BackUpKeys[request.form["username"]] = publicKeyPkcs1PEM
            # print(publicKeyPkcs1PEM)
            # print(Credentials)
            # print(UserIdKeyToUserName)
            fileName = SHA256.new(privateKeyPkcs1PEM.encode()).hexdigest()
            filePath = f"keys/{fileName}.txt"
            f = open(filePath, "w")
            f.write(privateKeyPkcs1PEM)
            f.close()
            UserObj[request.form["username"]] = {}
            UserObj[request.form["username"]]["filepath"] = filePath
            UserObj[request.form["username"]]["userId"] = request.form["KeyUserID"]
            return redirect(url_for("login"))
    return render_template("signUp.html", error=error)

@app.route("/download/<userId>", methods=["GET", "POST"])
def downloadKey(userId):
        username = userId
        if BackUpKeys[username]:
            filePath = UserObj[username]["filepath"]
            send_file(filePath, as_attachment=True)

@app.route("/login/", methods=["GET", "POST"])
def login():
    error = None
    print(Credentials)
    if request.method == "POST":
        if request.form["username"] not in Credentials:
            error = "Invalid username. Please try again."
        else:
            if Credentials.get(request.form["username"]) != request.form["password"]:
                error = "Invalid password. Please try again."
                return redirect(url_for("login"))
            else:
                global SignedInUser
                SignedInUser = request.form["username"]
                print("Signed in user id " + SignedInUser)
                return redirect(url_for("about", userIdentity=SignedInUser))
    return render_template("login.html", error=error )


@app.route("/logout/")
def logout():
    global SignedInUser
    SignedInUser = None
    return redirect(url_for("login"))


@app.route("/registerKey/", methods=["GET", "POST"])
def registerKey():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        req = request.json
        print(req)
        KeyUserID = req["userID"]
        keyID = req["keyID"]
        DomainName = req["domainName"]

        if UserKeyIDs == {}:
            error = {"error": "UserID is not registered with any user in key manager server"}
            response = app.response_class(
                response=json.dumps(error),
                status=400,
                mimetype='application/json'
            )
            return response
        UserName = UserIdKeyToUserName[KeyUserID]
        UserKeyIDs[UserName].append((keyID, DomainName, True))

        publicKey, privateKey = rsa.newkeys(512)
        privateKeyPkcs1PEM = privateKey.save_pkcs1().decode()
        publicKeyPkcs1PEM = publicKey.save_pkcs1().decode()
        UserNameServerKeys[(KeyUserID, DomainName)] = privateKeyPkcs1PEM
        res = {
            "BackupPublicKeyUser": BackUpKeys[UserName].split("\n"),
            "BackupPublicKeyServer": publicKeyPkcs1PEM.split("\n"),
        }
        print(UserKeyIDs[UserName])
        print(res)
        return json.dumps(res)
    else:
        return "Content-Type not supported!"


@app.route("/alive/", methods=["GET", "POST"])
def alive():
    res = {"status": True}
    return json.dumps(res)
