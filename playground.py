import nex

doc = nex.GetActiveDocument()
label = "digin108192"
nex.Rename(doc, doc[label], "Hi")
