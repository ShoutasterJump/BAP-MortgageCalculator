def generate_amortization_table_html(amortization_table):
    def format_currency(value):
        if isinstance(value, (int, float)):
            return f"${value:,.2f}"
        return value

    rows = []
    for entry in amortization_table:
        row = f"""
        <tr>
            <td>{entry['Date']}</td>
            <td>{format_currency(entry['Balance'])}</td>
            <td>{format_currency(entry['Interest'])}</td>
            <td>{format_currency(entry['Principal'])}</td>
            <td>{format_currency(entry['Extra'])}</td>
            <td>{format_currency(entry['Repayment'])}</td>
            <td>{format_currency(entry['New Balance'])}</td>
            <td>{format_currency(entry['Accumulated Interest'])}</td>
            <td>{format_currency(entry['Accumulated Principal Payments'])}</td>
        </tr>
        """
        rows.append(row)
    return ''.join(rows)
