var swiper = new Swiper('.swiper-container', {
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });

 
  document.getElementById('login-button').addEventListener('click', function() {
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;

      if (email === '' || password === '') {
          alert('Please fill in both fields.');
          return;
      }

      // Here you can add your authentication logic
      console.log('Email:', email);
      console.log('Password:', password);

      // For demonstration, we'll just log a success message
      alert('Login successful!');
  });

//   signup page
document.getElementById('signup-button').addEventListener('click', function() {
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm-password').value;

    if (name === '' || email === '' || password === '' || confirmPassword === '') {
        alert('Please fill in all fields.');
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    // Here you can add your registration logic
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('Password:', password);

    // For demonstration, we'll just log a success message
    alert('Signup successful!');
});

