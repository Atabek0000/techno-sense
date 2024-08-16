function validateForm() {
  const cardNumber = document.getElementById("card-number").value;
  const cardExp = document.getElementById("card-exp").value;
  const cardCcv = document.getElementById("card-ccv").value;

  const cardNumberPattern = /^\d{4}\s\d{4}\s\d{4}\s\d{4}$/;
  const cardExpPattern = /^(0[1-9]|1[0-2])\/\d{2}$/;
  const cardCcvPattern = /^\d{3}$/;

  if (!cardNumberPattern.test(cardNumber)) {
    alert("Invalid card number. Please enter in the format: 1234 1234 1234 1234.");
    return false;
  }

  if (!cardExpPattern.test(cardExp)) {
    alert("Invalid expiration date. Please enter in the format: MM/YY.");
    return false;
  }

  if (!cardCcvPattern.test(cardCcv)) {
    alert("Invalid CCV. Please enter a 3-digit code.");
    return false;
  }

  return true;
}
