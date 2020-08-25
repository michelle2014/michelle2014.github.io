document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  document.querySelector('#compose-form').addEventListener("submit", function (event) {
    event.preventDefault();
  });
  
  // By default, load the inbox
  load_mailbox('inbox');
  
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send the email
  submit_email();
}

function submit_email() {
  // Select the submit button and input to be used later
  const submit = document.querySelector('#submit');
  const recipients = document.querySelector('#compose-recipients');
  const subject = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body');

  // Disable submit button by default
  submit.disabled = true;

  // Listen for input to be typed into each of the input fields
  recipients.onkeyup = () => {
    if (recipients.value.length > 0 && subject.value.length > 0 && body.value.length > 0) {
      submit.disabled = false;
    }
    else {
      submit.disabled = true;
    }
  }

  subject.onkeyup = () => {
    if (recipients.value.length > 0 && subject.value.length > 0 && body.value.length > 0) {
      submit.disabled = false;
    }
    else {
      submit.disabled = true;
    }
  }

  body.onkeyup = () => {
    if (recipients.value.length > 0 && subject.value.length > 0 && body.value.length > 0) {
      submit.disabled = false;
    }
    else {
      submit.disabled = true;
    }
  }

  // Using post method to actually submit the form and pass input values
  document.querySelector('#compose-form').addEventListener('submit', () => {
    recipients.forEach(
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
          recipients: recipients.value,
          subject: subject.value,
          body: body.value
        })
      })
      .then(response => response.json())
      .then(result => {
        // Print result
        // console.log(result.message);
        const message = result.message;
        const error = result.error;
        if (message) {
          document.querySelector('#compose-result').innerHTML = `<div class="alert alert-success alert-dismissible"><a href="" class="close" data-dismiss="alert" aria-label="close">&times;</a>${message}</div>`;
          load_mailbox("sent");
        }
        else if (error) {
          compose_email()
          document.querySelector('#compose-result').innerHTML = `<div class="alert alert-danger alert-dismissible"><a href="" class="close" data-dismiss="alert" aria-label="close">&times;</a>${error}</div>`;
        }
      })
    );
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Show emails in each mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Get emails information
    for (var i = 0, len=emails.length; i < len; i++) {
      const sender = emails[i].sender;
      const subject = emails[i].subject;
      const timestamp = emails[i].timestamp;
      const email_id = emails[i].id;
      const read = emails[i].read;

      // Create div in html and append emails information to it
      const element = document.createElement('div');
      element.innerHTML = `<span class="bold_span">${sender}</span><span>${subject}</span><span id="time_span">${timestamp}</span>`;
      document.querySelector('#emails-view').append(element);

      // If email read, change background color to grey, else background color white
      if (read) {
        element.style.backgroundColor = '#d9d9d9';
      }
      else {
        element.style.backgroundColor = 'white';
      }

      // Get each email information by id
      fetch(`/emails/${email_id}`)
      .then(response => response.json())
      .then(email => {
        // console.log(email);
        // Get information of each email
        const from = email.sender;
        const to = email.recipients;
        const email_subject = email.subject;
        const email_timestamp = email.timestamp;
        const email_body = email.body;
        const archived = email.archived;
        
        // Click email, display email content
        element.addEventListener('click', function() {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#email-content').style.display = 'block';
          document.querySelector('#compose-view').style.display = 'none';

          // Mark the email as read if clicked
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          });

          // If it is inbox or archived emails, display archive (or unarchive) and read buttons
          if (from !== document.querySelector('#user_email').value) {
            // Create div in html and append information of each email and a reply link button to it
            const content = document.createElement('div');

            // If archived email, display the button as "unarchive", when click the button, unarchive the email
            if (archived) {
              content.innerHTML = `<button id="unarchive" class="btn btn-sm btn-outline-primary">Unarchive</button><p><span class="bold_span">From: </span>${from}</p><p><span class="bold_span">To: </span>${to}</p><p><span class="bold_span">Subject: </span>${email_subject}</p><p><span class="bold_span">Timestamp: </span>${email_timestamp}</p><div id="email_reply"><button class="btn btn-sm btn-outline-primary">Reply</button></div><hr><p>${email_body}</p>`;
              document.querySelector('#email-content').append(content);
              document.querySelector('#unarchive').onclick = () => {
                fetch(`/emails/${email_id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: false
                  })
                })
                .then(() => {
                  load_mailbox('inbox');
                });
              }
            }
            // Otherwise display the button as "archive", when click the button, archive the email
            else {
              content.innerHTML = `<button id="archive" class="btn btn-sm btn-outline-primary">Archive</button><p><span class="bold_span">From: </span>${from}</p><p><span class="bold_span">To: </span>${to}</p><p><span class="bold_span">Subject: </span>${email_subject}</p><p><span class="bold_span">Timestamp: </span>${email_timestamp}</p><div id="email_reply"><button class="btn btn-sm btn-outline-primary">Reply</button></div><hr><p>${email_body}</p>`;
              document.querySelector('#email-content').append(content);
              document.querySelector('#archive').onclick = () => {
                fetch(`/emails/${email_id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: true
                  })
                })
                .then(() => {
                  load_mailbox('inbox');
                });
              }
            }
          }

          // Else if it is sent emails
          else {
            // Create div in html and append information of each email and a reply link button to it
            const content = document.createElement('div');
            content.innerHTML = `<p><span class="bold_span">From: </span>${from}</p><p><span class="bold_span">To: </span>${to}</p><p><span class="bold_span">Subject: </span>${email_subject}</p><p><span class="bold_span">Timestamp: </span>${email_timestamp}</p><div id="email_reply"><button class="btn btn-sm btn-outline-primary">Reply</button></div><hr><p>${email_body}</p>`;
            document.querySelector('#email-content').append(content);
          }

          // Display compose form after clicking reply button of the email
          document.querySelector('#email_reply').onclick = () => {
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#email-content').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';

            // Prefill recipients and subject of the compose form
            document.querySelector('#compose-recipients').value = from;
            // console.log(document.querySelector('#compose-subject').value);
            // If the subject line already begins with Re: , no need to add it again
            if (email_subject.substring(0,3) !== "Re:") {
              document.querySelector('#compose-subject').value = `Re: ${email_subject}`;
            }
            else {
              document.querySelector('#compose-subject').value = `${email_subject}`;
            }
            
            // Prefill body of the compose
            document.querySelector('#compose-body').value = `On ${email_timestamp} ${sender} wrote: ${email_body}`;
            
            // Reply the email
            submit_email();

          }
        });
        // Clear out email-content fields
        document.querySelector('#email-content').innerHTML = '';
      })
      

    }
  });
}