from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():

    connection = sqlite3.connect("soc.db")

    connection.row_factory = sqlite3.Row

    return connection


@app.route("/")
def dashboard():

    severity = request.args.get("severity", "")
    status = request.args.get("status", "")
    search = request.args.get("search", "")

    connection = get_db_connection()

    query = "SELECT * FROM alerts WHERE 1=1"

    parameters = []

    if severity:

        query += " AND severity = ?"

        parameters.append(severity)

    if status:

        query += " AND status = ?"

        parameters.append(status)

    if search:

        query += """
        AND (
            alert_name LIKE ?
            OR source_ip LIKE ?
            OR destination_ip LIKE ?
        )
        """

        search_value = f"%{search}%"

        parameters.extend([
            search_value,
            search_value,
            search_value
        ])

    query += " ORDER BY id DESC"

    alerts = connection.execute(
        query,
        parameters
    ).fetchall()


    total_alerts = connection.execute(
        "SELECT COUNT(*) FROM alerts"
    ).fetchone()[0]


    critical_alerts = connection.execute(
        """
        SELECT COUNT(*)
        FROM alerts
        WHERE severity = 'Critical'
        """
    ).fetchone()[0]


    high_alerts = connection.execute(
        """
        SELECT COUNT(*)
        FROM alerts
        WHERE severity = 'High'
        """
    ).fetchone()[0]


    medium_alerts = connection.execute(
        """
        SELECT COUNT(*)
        FROM alerts
        WHERE severity = 'Medium'
        """
    ).fetchone()[0]


    low_alerts = connection.execute(
        """
        SELECT COUNT(*)
        FROM alerts
        WHERE severity = 'Low'
        """
    ).fetchone()[0]


    connection.close()


    return render_template(

        "dashboard.html",

        alerts=alerts,

        total_alerts=total_alerts,

        critical_alerts=critical_alerts,

        high_alerts=high_alerts,

        medium_alerts=medium_alerts,

        low_alerts=low_alerts,

        selected_severity=severity,

        selected_status=status,

        search=search

    )


@app.route("/alert/<int:alert_id>")
def alert_details(alert_id):

    connection = get_db_connection()

    alert = connection.execute(
        """
        SELECT *
        FROM alerts
        WHERE id = ?
        """,
        (alert_id,)
    ).fetchone()

    connection.close()

    if alert is None:

        return "Alert not found", 404


    return render_template(

        "alert_details.html",

        alert=alert

    )


@app.route(
    "/alert/<int:alert_id>/status",
    methods=["POST"]
)
def update_alert_status(alert_id):

    new_status = request.form.get("status")

    allowed_statuses = [

        "Open",

        "Investigating",

        "Resolved"

    ]

    if new_status not in allowed_statuses:

        return "Invalid status", 400


    connection = get_db_connection()


    connection.execute(
        """
        UPDATE alerts
        SET status = ?
        WHERE id = ?
        """,
        (
            new_status,
            alert_id
        )
    )


    connection.commit()

    connection.close()


    return redirect(

        url_for(

            "alert_details",

            alert_id=alert_id

        )

    )


@app.route(
    "/alert/<int:alert_id>/notes",
    methods=["POST"]
)
def update_analyst_notes(alert_id):

    analyst_notes = request.form.get(
        "analyst_notes",
        ""
    )


    connection = get_db_connection()


    connection.execute(
        """
        UPDATE alerts
        SET analyst_notes = ?
        WHERE id = ?
        """,
        (
            analyst_notes,
            alert_id
        )
    )


    connection.commit()

    connection.close()


    return redirect(

        url_for(

            "alert_details",

            alert_id=alert_id

        )

    )


if __name__ == "__main__":

    app.run(debug=True)