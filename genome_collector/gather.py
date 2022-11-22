from Bio import SeqIO
import os
import shutil
import json
import re


# NCBI regex
REGEX = "GC[A,F]_[0-9]{9}.[0-9]"

target = "./ncbi_dataset/ncbi_dataset/data"


class Genome:
    def __init__(self):
        self.accession = ""
        self.path_fasta = []
        self.path_annotation = []
        self.path_protein = []
        self.path_cds = []
        self.path_report = []
        self.path_rna = []

        self.fasta = []

    def __repr__(self):
        return f"Genome {self.accession} \n fasta: {len(genome.path_fasta)}\n annotation: {len(genome.path_annotation)}\n protein: {len(genome.path_protein)}\n cds: {len(genome.path_cds)}\n report: {len(genome.path_report)}\n rna: {len(genome.path_rna)}\n"

    def clean(self):

        self.merge_genome()
        self.rename()

        if len(self.path_annotation) > 1:
            raise Exception

        print("---------------------")

    # merge fasta files if multiple genomic sequences exists
    def merge_genome(self):

        if len(self.path_fasta) > 0:
            for path in self.path_fasta:
                self.fasta += list(SeqIO.parse(path, "fasta"))

    # remove descriptions of each fasta
    def rename(self):
        if len(self.fasta) > 0:
            for fasta in self.fasta:
                fasta.description = ""

    # save files
    def save(self, path):
        os.mkdir(f"{path}/{self.accession}")
        SeqIO.write(self.fasta, f"{path}/{self.accession}/genome.fna", "fasta")
        for f in self.path_annotation:
            shutil.copy(f, f"{path}/{self.accession}/annotation.gff")


# Check if the file is properly downloaded ncbi genome dataset
if not ("dataset_catalog.json" in os.listdir(target)):
    raise Exception

# Operate files by catalog json
with open(f"{target}/dataset_catalog.json", "r", encoding="UTF-8") as f:
    json_dict = json.load(f)
    for assembly in json_dict["assemblies"]:
        # For catalog files
        if (
            not ("accession" in assembly.keys())
            and assembly["files"][0]["fileType"] == "DATA_REPORT"
        ):
            pass
        # For file information
        else:
            genome = Genome()
            genome.accession = assembly["accession"]

            for fileinfo in assembly["files"]:
                if fileinfo["fileType"] == "GENOMIC_NUCLEOTIDE_FASTA":
                    genome.path_fasta.append(f"{target}/{fileinfo['filePath']}")
                elif fileinfo["fileType"] == "GFF3":
                    genome.path_annotation.append(f"{target}/{fileinfo['filePath']}")
                elif fileinfo["fileType"] == "PROTEIN_FASTA":
                    genome.path_protein.append(f"{target}/{fileinfo['filePath']}")
                elif fileinfo["fileType"] == "CDS_NUCLEOTIDE_FASTA":
                    genome.path_cds.append(f"{target}/{fileinfo['filePath']}")
                elif fileinfo["fileType"] == "SEQUENCE_REPORT":
                    genome.path_report.append(f"{target}/{fileinfo['filePath']}")
                elif fileinfo["fileType"] == "RNA_NUCLEOTIDE_FASTA":
                    genome.path_rna.append(f"{target}/{fileinfo['filePath']}")
                else:
                    print(fileinfo["fileType"])
                    print(assembly)
                    raise Exception

            try:
                genome.clean()
                genome.save("./refined")
            except:
                print(f"Passing genome {genome.accession}")


'''

    for (root, dirs, files) in os.walk("./query"):
        linux_root = root.replace("\\", "/")

        if re.search(REGEX, linux_root.split("/")[-1]):
            print(linux_root.split("/")[-1], end=" ")
            """
            try:
                shutil.copytree(linux_root, f'./collected/{linux_root.split("/")[-1]}')
            except:
                for file in files:
                    shutil.copy(
                        f"{linux_root}/{file}", f'./collected/{linux_root.split("/")[-1]}'
                    )
            """

with open("out.json", "r", encoding="UTF-8") as f:
    json_dict = json.load(f)
    for assembly in json_dict["assemblies"]:
        for k in assembly["assembly"].keys():
            print(k)
            print(assembly["assembly"][k])

        # if "annotation_metadata" in assembly["assembly"]:
        #    print(assembly["assembly"]["annotation_metadata"])
'''
