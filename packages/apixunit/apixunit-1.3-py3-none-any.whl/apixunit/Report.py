from apixunit.CONST_j import CONST
from pathlib import Path

import time, shutil

mypath = Path.cwd()


def Generate_Report(excel, report, pass_fail, test_case_no, casedirpath, rowindex):
    try:
        if pass_fail.lower() == "pass":
            passdirpath = casedirpath / Path("Pass")
            if not passdirpath.is_dir():
                passdirpath.mkdir()

            capturename = r"TC%s_Dataset_%s_Step_Pass.png" \
                          % (str(test_case_no), str(int(excel.Get_Value_By_ColName("Data set", rowindex))))
            snapshotpath = str(passdirpath.absolute()) + "\\" + capturename
            link = r'=HYPERLINK("%s","%s")' % (snapshotpath, capturename)

        elif pass_fail.lower() == "fail":
            faildirpath = casedirpath / Path("Fail")
            if not faildirpath.is_dir():
                faildirpath.mkdir()

            capturename = r"TC%s_Dataset_%s_Step_Fail.png" \
                          % (str(test_case_no), str(int(excel.Get_Value_By_ColName("Data set", rowindex))))
            snapshotpath = str(faildirpath.absolute()) + "\\" + capturename
            link = r'=HYPERLINK("%s","%s")' % (snapshotpath, capturename)

            stepspath = Path(casedirpath) / Path("Steps")
            stepsfiles = list(stepspath.rglob('TC%s_Dataset_%s_Step*.png' % (str(test_case_no), str(rowindex))))
            for s in stepsfiles:
                shutil.copy(str(s), faildirpath)

        report.Select_Sheet_By_Name(str(test_case_no))
        report.Set_Value_By_ColName(pass_fail, "Result", rowindex)
        report.Set_Value_By_ColName(link, "Screen capture", rowindex)
        report.Set_Value_By_ColName("done", "executed", rowindex)

        randomfilepath = Path(casedirpath)
        randomfiles = list(randomfilepath.rglob('*.random'))
        if len(randomfiles) != 0:
            randomrecords = []
            for l in randomfiles:
                p = str(list(l.parts)[-1:])
                p = p[:p.find(".random")]
                randomrecords.append(p.split("_"))

            randomrecords = list(randomrecords)

            for i in range(len(randomrecords)):
                if int(randomrecords[i][0][-1:]) == rowindex:
                    report.Set_Value_By_ColName("%s(%s)" % (
                        excel.Get_Value_By_ColName(randomrecords[i][1], rowindex), randomrecords[i][2]),
                                                randomrecords[i][1], rowindex)
    except Exception as msg:
        print(msg)


def Generate_Final_Report(excel, report, test_case_no):
    report.Select_Sheet_By_Name("result-timestamp")
    wtrowindex = report.Get_Row_Numbers()

    for rowindex in range(1, excel.Get_Row_Numbers()):
        # print(wtrowindex)
        bro = excel.Get_Value_By_ColName("Browser", rowindex)
        res = excel.Get_Value_By_ColName("Result", rowindex)
        exe = excel.Get_Value_By_ColName("executed", rowindex)

        if exe is not None:
            report.Set_Value_By_ColName(test_case_no, "Case No", wtrowindex)
            report.Set_Value_By_ColName(rowindex, "Data set", wtrowindex)
            report.Set_Value_By_ColName(excel.Get_Value_By_ColName("Expected result", rowindex), "Expected result",
                                        wtrowindex)
            if exe.lower() == "skip":
                report.Set_Value_By_ColName("Skipped", "Result", wtrowindex)
                report.Set_Value_By_ColName("Skipped", "Browser", wtrowindex)
            elif res is None:
                report.Set_Value_By_ColName("Skipped", "Result", wtrowindex)
                report.Set_Value_By_ColName("Skipped", "Browser", wtrowindex)
            else:
                report.Set_Value_By_ColName(res, "Result", wtrowindex)
                if bro is not None:
                    report.Set_Value_By_ColName(bro, "Browser", wtrowindex)
                else:
                    report.Set_Value_By_ColName("Chrome", "Browser", wtrowindex)
            report.Set_Value_By_ColName(excel.Get_Value_By_ColName("Description", rowindex), "Description", wtrowindex)
            report.Set_Value_By_ColName(excel.Get_Value_By_ColName("Screen capture", rowindex), "Screen capture",
                                        wtrowindex)
            report.Set_Value_By_ColName(exe, "executed", wtrowindex)
            report.Set_Value_By_ColName(excel.Get_Value_By_ColName("Assertion", rowindex), "Assertion", wtrowindex)
            report.Set_Value_By_ColName(excel.Get_Value_By_ColName("ID", rowindex), "ID", wtrowindex)
            report.Set_Value_By_ColName(excel.Get_Value_By_ColName("PW", rowindex), "PW", wtrowindex)

            wtrowindex = wtrowindex + 1


def Create_New_Report(folderpath):
    otime = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    reprotfolderpath = Path(folderpath) / Path(otime)
    if reprotfolderpath.is_dir():
        pass
    else:
        reprotfolderpath.mkdir()
    reportfilepath = folderpath + "\\" + reprotfolderpath.name + r"\Report_" + otime + ".xlsx"

    #shutil.copy(CONST.EXCELPATH, reportfilepath)

    if Path(reportfilepath).is_file():
        return str(reportfilepath)
    else:
        raise Exception("No excel file")
