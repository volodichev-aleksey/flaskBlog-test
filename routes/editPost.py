# Import the necessary modules and functions
from helpers import (
    flash,
    abort,
    session,
    sqlite3,
    request,
    message,
    redirect,
    Blueprint,
    RECAPTCHA,
    requestsPost,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    CreatePostForm,
    render_template,
    currentTimeStamp,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_POST_EDIT,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
)

# Create a blueprint for the edit post route
editPostBlueprint = Blueprint("editPost", __name__)


@editPostBlueprint.route("/editpost/<int:postID>", methods=["GET", "POST"])
def editPost(postID):
    """
    This function handles the edit post route.

    Args:
        postID (int): the ID of the post to edit

    Returns:
        The rendered edit post template or a redirect to the homepage if the user is not authorized to edit the post

    Raises:
        abort(404): if the post does not exist
        abort(401): if the user is not authorized to edit the post
    """
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_POSTS_ROOT)
            cursor = connection.cursor()
            cursor.execute("select id from posts")
            posts = str(cursor.fetchall())
            match str(postID) in posts:
                case True:
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select * from posts where id = ? """,
                        [(postID)],
                    )
                    post = cursor.fetchone()
                    message("2", f'POST: "{postID}" FOUND')
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select userName from users where userName = ? """,
                        [(session["userName"])],
                    )
                    match post[5] == session["userName"] or session["userRole"] == "admin":
                        case True:
                            form = CreatePostForm(request.form)
                            form.postTitle.data = post[1]
                            form.postTags.data = post[2]
                            form.postContent.data = post[3]
                            form.postCategory.data = post[9]
                            match request.method == "POST":
                                case True:
                                    postTitle = request.form["postTitle"]
                                    postTags = request.form["postTags"]
                                    postContent = request.form["postContent"]
                                    postCategory = request.form["postCategory"]
                                    postBanner=request.files["postBanner"].read()
                                    match postContent == "":
                                        case True:
                                            flash("post content not be empty", "error")
                                            message(
                                                "1",
                                                f'POST CONTENT NOT BE EMPTY USER: "{session["userName"]}"',
                                            )
                                        case False:
                                            match RECAPTCHA and RECAPTCHA_POST_EDIT:
                                                case True:
                                                    secretResponse = request.form[
                                                                        "g-recaptcha-response"
                                                                    ]
                                                    verifyResponse = requestsPost(
                                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                                    ).json()
                                                    match verifyResponse[
                                                                        "success"
                                                                    ] == True or verifyResponse[
                                                                        "score"
                                                                    ] > 0.5:
                                                        case True:
                                                            message("2",f"POST EDIT RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            connection = sqlite3.connect(DB_POSTS_ROOT)
                                                            cursor = connection.cursor()
                                                            cursor.execute(
                                                                """update posts set title = ? where id = ? """,
                                                                (postTitle, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set tags = ? where id = ? """,
                                                                (postTags, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set content = ? where id = ? """,
                                                                (postContent, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set category = ? where id = ? """,
                                                                (postCategory, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set banner = ? where id = ? """,
                                                                (postBanner, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set lastEditTimeStamp = ? where id = ? """,
                                                                [(currentTimeStamp()), (post[0])],
                                                            )
                                                            connection.commit()
                                                            message("2", f'POST: "{postTitle}" EDITED')
                                                            flash("Post edited", "success")
                                                            return redirect(f"/post/{post[0]}")
                                                        case False:
                                                            message("1",f"POST EDIT RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            abort(401)
                                                case False:
                                                    connection = sqlite3.connect(DB_POSTS_ROOT)
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update posts set title = ? where id = ? """,
                                                        (postTitle, post[0]),
                                                    )
                                                    cursor.execute(
                                                        """update posts set tags = ? where id = ? """,
                                                        (postTags, post[0]),
                                                    )
                                                    cursor.execute(
                                                        """update posts set content = ? where id = ? """,
                                                        (postContent, post[0]),
                                                    )
                                                    cursor.execute(
                                                                """update posts set category = ? where id = ? """,
                                                                (postCategory, post[0]),
                                                    )
                                                    cursor.execute(
                                                                """update posts set banner = ? where id = ? """,
                                                                (postBanner, post[0]),
                                                    )
                                                    cursor.execute(
                                                                """update posts set lastEditTimeStamp = ? where id = ? """,
                                                                [(currentTimeStamp()), (post[0])],
                                                    )
                                                    connection.commit()
                                                    message("2", f'POST: "{postTitle}" EDITED')
                                                    flash("Post edited", "success")
                                                    return redirect(f"/post/{post[0]}")
                            return render_template(
                                "/editPost.html.jinja",
                                id = post[0],
                                title=post[1],
                                tags=post[2],
                                content=post[3],
                                form=form,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
                        case False:
                            flash("this post not yours", "error")
                            message(
                                "1",
                                f'THIS POST DOES NOT BELONG TO USER: "{session["userName"]}"',
                            )
                            return redirect("/")
                case False:
                    message("1", f'POST: "{postID}" NOT FOUND')
                    return render_template("notFound.html.jinja")
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for edit a post", "error")
            return redirect(f"/login/redirect=&editpost&{postID}")
