function tokenIsSet() {
  return (localStorage.getItem("token") != null)
}

function getDayOfWeek(date) {
  const dayOfWeek = new Date(date).getDay();
  return isNaN(dayOfWeek) ? null :
    ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'][dayOfWeek];
}

export {
  tokenIsSet,
  getDayOfWeek
}