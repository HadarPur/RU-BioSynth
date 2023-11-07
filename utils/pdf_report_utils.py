from fpdf import FPDF

class Report:
    def __init__(self, input_seq, target_seq, marked_input_seq, marked_target_seq):
        self.input_seq = input_seq
        self.target_seq = target_seq
        self.marked_input_seq = marked_input_seq
        self.marked_target_seq = marked_target_seq

        self.pdf = FPDF()

    def create_pdf(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 16)
        ## Title
        self.pdf.cell(40, 10, 'Daily S&P 500 prices report')
        ## Line breaks
        self.pdf.ln(20)
        self.pdf.set_font('Arial', '', 12)
        self.diff_seq_to_pdf()

        # output_df_to_pdf(pdf, sp500_history_summary_pdf)
        # 3. Output the PDF file
        self.pdf.output('fpdf_pdf_report.pdf', 'F')

    def diff_seq_to_pdf(self):
        # A cell is a rectangular area, possibly framed, which contains some text
        # Set the width and height of cell
        table_cell_width = 25
        table_cell_height = 6

        self.pdf.cell(table_cell_width, table_cell_height, self.input_seq)
        self.pdf.ln(20)
        self.pdf.cell(table_cell_width, table_cell_height, self.target_seq)
        self.pdf.ln(20)

        # Select a font as Arial, bold, 8
        self.pdf.cell(table_cell_width, table_cell_height, self.marked_input_seq)
        self.pdf.ln(20)
        self.pdf.cell(table_cell_width, table_cell_height, self.marked_target_seq)
