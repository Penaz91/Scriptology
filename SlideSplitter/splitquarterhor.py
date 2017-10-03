def splitquarterhor(inputfilename):
    from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
    from tempfile import mkdtemp
    from os.path import join, isfile, splitext
    from os import listdir
    output = PdfFileWriter()
    input1 = PdfFileReader(open(inputfilename+".pdf", "rb"))
    count = 0
    numpg = input1.getNumPages()
    tempdir = mkdtemp()
# codice per lo splitting
# ricavo la pagina
    for i in range(0, numpg):
        pg = input1.getPage(i)
        # Prima Pagina (alto sinistra)
        pg.mediaBox.setUpperRight((297.61, 421))
        outputstream = open(tempdir + "/" + str(count)+".pdf", "wb")
        output.addPage(pg)
        output.write(outputstream)
        pg.mediaBox.setUpperRight((595.22, 842))
        outputstream.close()
        del output, outputstream
        count += 1
        # Reset Dell'output
        output = PdfFileWriter()
        # Seconda Pagina (Alto Destra)
        pg.mediaBox.setLowerRight((297.61, 421))
        outputstream = open(tempdir + "/" + str(count)+".pdf", "wb")
        output.addPage(pg)
        output.write(outputstream)
        pg.mediaBox.setLowerRight((595.22, 842))
        outputstream.close()
        del output, outputstream
        count += 1
        # Reset Dell'output
        output = PdfFileWriter()
        # Terza Pagina (Basso Sinistra)
        pg.mediaBox.setLowerLeft((297.61, 0))
        pg.mediaBox.setUpperRight((595.22000, 421))
        outputstream = open(tempdir + "/" + str(count)+".pdf", "wb")
        output.addPage(pg)
        output.write(outputstream)
        outputstream.close()
        pg.mediaBox.setUpperRight((595.22000, 842))
        pg.mediaBox.setLowerLeft((0, 0))
        count += 1
        del output, outputstream
        # Reset Dell'output
        output = PdfFileWriter()

        # Quarta Pagina (basso Destra)
        pg.mediaBox.setLowerLeft((297.61, 421))
        outputstream = open(tempdir + "/" + str(count)+".pdf", "wb")
        output.addPage(pg)
        output.write(outputstream)
        pg.mediaBox.setLowerLeft((0, 0))
        outputstream.close()
        del output, outputstream
        count += 1
        # Reset Dell'output
        output = PdfFileWriter()

# Giunzione delle pagine
    filelist = [splitext(file)[0] for file in listdir(tempdir) if isfile(join(tempdir, file))]
    filelist.sort(key=int)

    output = PdfFileMerger()
    for file in filelist:
        input = open(join(tempdir, file + ".pdf"), "rb")
        output.append(input)

    os = open(inputfilename+"_split.pdf", "wb")
    output.write(os)
    os.close()
