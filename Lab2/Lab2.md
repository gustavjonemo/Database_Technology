<h1>Lab 2</h1>

<h2>6</h2>
<p>
theaters(_t_name_, capacity)
movies(_imbd_key_, title, year, duration)
screenings(/_t_name_/, /_imbd_key_/, date, start)
tickets(_ticket_id_, /username/, /t_name/, /imbd_key/)
customers(_username_, name, password)
</p>

<h2>7</h2>
<p>
seats availible = capacity - count(ticket_id). Pros: simple Cons: no history, prone to error

event sourcing: new "event" table or time parameter, tracks ticket purchases. Pros: Robust, look at status at different points in time Cons: more complex
</p>