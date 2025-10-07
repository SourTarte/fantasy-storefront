const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
    console.log("Delete button is "+button);
  button.addEventListener("click", (e) => {
    console.log("button is clicked");
    let reviewid = e.target.getAttribute("data-review_id");
    console.log(`e.target is ${e.target} and reviewid is ${reviewid}`);
    deleteConfirm.href = `delete_comment/${reviewid}`;
    deleteModal.show();
  });
}



