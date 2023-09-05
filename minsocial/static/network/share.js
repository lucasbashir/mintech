
    let fileUrl; // Variable to store the file URL

    function shareFile(url) {
        fileUrl = url; // Set the file URL to the variable
        const modal = document.getElementById("shareModal");
        modal.style.display = "block";
        const closeModalBtn = modal.querySelector(".close");
        closeModalBtn.onclick = function() {
            modal.style.display = "none";
        };
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };
    }

    function copyLink() {
        if (fileUrl) {
            navigator.clipboard.writeText(fileUrl);
            const linkCopiedAlert = document.getElementById("linkCopiedAlert");
            linkCopiedAlert.style.display = "block";
            setTimeout(function() {
                linkCopiedAlert.style.display = "none";
            }, 2000);
        }
    }

    function shareWithinWebsite() {
        if (fileUrl) {
            // Your custom logic to share the file within the website goes here
            // For example, you can use an API to notify other users about the shared file
            // and display a success message after sharing.
            alert("Shared within the website!");
        }
    }

    