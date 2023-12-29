import ast
from cdxg.logging import log
import cdxg
from aapigtf.common import get_results


class Results(cdxg.TestCase):

    def resultsvalidations(self, testcase, getresults, test_types, var_types, input_types, case, exresults,
                           xlcreate, tepoint, tpload, tparams, comments, roles, timeelapsed, sprints, httpcodes, incidentids, alljson):
        if input_types == 'Data':
            print('***********************************************************************************************')
            print('System_Response:' + str(getresults))
            print('***********************************************************************************************')
            if 'Expected results given is not Matched' in str(getresults):
                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                            results='FAILED', fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                            comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                log.error('Given expected results is not matched...')
                self.fail('Given expected results is not matched...')
            else:
                if str(test_types) == 'Json':
                    if var_types != 'ST4':
                        exresults = ast.literal_eval(str(exresults))
                        print('Expected_Result:' + str(exresults))
                        log.info('Results : ' + str(results))
                        self.compareresults(roles, testcase, var_types, getresults, exresults, case, xlcreate, tepoint,
                                            tpload, comments, timeelapsed, tparams, sprints, httpcodes, incidentids)
                    else:
                        if getresults == 'Match Found':
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                        results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        sprints=sprints, incidentids=incidentids, alljson=alljson)
                            log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                            self.assert_('Actual Items in the list are valid and expected')
                        else:
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                        results='FAILED', fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                            log.error('CASE[' + str(case) + '] ' + str(testcase) + ': FAILED')
                            self.fail('Invalid Item take place in list or No match found as expected')
                else:
                    if var_types not in ['ST2', 'ST5']:
                        if var_types == 'ST4':
                            if getresults == 'Match Found':
                                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                            results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                            sprints=sprints, incidentids=incidentids, alljson=alljson)
                                log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                                self.assert_('Actual Items in the list are valid and expected')
                            elif getresults == exresults:
                                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                            results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                            sprints=sprints, incidentids=incidentids, alljson=alljson)
                                log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                                self.assert_('Actual Items in the list are valid and expected')
                            else:
                                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                            results='FAILED',fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                            comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                                log.error('CASE[' + str(case) + '] ' + str(testcase) + ': FAILED')
                                self.fail('Invalid Item take place in list or No match found as expected')
                        else:
                            exp_results = str(exresults).split('*')
                            for gttn in range(0, len(exp_results)):
                                log.info('Results:' + str(exp_results[gttn]))
                                log.info('Expected_Result : ' + str(results))
                                log.info(getresults[gttn])
                                if getresults[gttn] == exp_results[gttn]:
                                    # getresults = getresults
                                    print(
                                        '*****************************************************************************')
                                    self.compareresults(roles, testcase, var_types, getresults[gttn], exp_results[gttn],
                                                        case, xlcreate, tepoint, tpload, comments, timeelapsed, tparams,
                                                        sprints, httpcodes, incidentids, alljson)
                    else:
                        print('Results:' + str(exresults))
                        log.info('Expected_Result : ' + str(results))
                        print('***************************************************************************************')
                        self.compareresults(roles, testcase, var_types, getresults, exresults, case, xlcreate, tepoint,
                                            tpload, comments, timeelapsed, tparams, sprints, httpcodes, incidentids, alljson)
        elif input_types == 'Schema':
            if 'Expected results given is not Matched' in str(getresults):
                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                            results='FAILED',fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                            comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                log.error('Given expected results is not matched...')
                self.fail('Given expected results is not matched...')
            else:
                getresults = ast.literal_eval(str(getresults))
                exresults = ast.literal_eval(str(exresults))
                print('***********************************************************************************************')
                print('System_Response:' + str(getresults))
                print('***********************************************************************************************')
                print('Results:' + str(exresults))
                log.info('Expected_Result : ' + str(results))
                print('***********************************************************************************************')
                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                            results='PASSED',fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                            sprints=sprints, incidentids=incidentids, alljson=alljson)
                log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                self.assertEqual(getresults[0], exresults)
        elif input_types == 'List':
            print('***********************************************************************************************')
            print('System_Response:' + str(getresults))
            print('***********************************************************************************************')
            if var_types == 'ST4':
                if getresults == 'Match Found':
                    get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                results='PASSED',fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                sprints=sprints, incidentids=incidentids, alljson=alljson)
                    log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                    self.assert_('Actual Items in the list are valid and expected')
                else:
                    get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                                results='FAILED',fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                            comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                    log.error('CASE[' + str(case) + '] ' + str(testcase) + ': FAILED')
                    self.fail('Invalid Item take place in list or No match found as expected')
            else:
                getresults = ast.literal_eval(str(getresults))
                exresults = ast.literal_eval(str(exresults))
                for xeResults in getresults:
                    if xeResults == exresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults[0],
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                        self.assertEqual(getresults[0], exresults)
                    else:
                        gbn = None
                        eResults = exresults
                        getxln = []
                        for gres in xeResults:
                            for i in range(0, len(eResults)):
                                if eResults[i] == gres:
                                    gbn = 'Valid'
                                    break
                                else:
                                    gbn = 'Invalid'
                            getxln.append(gbn)
                        if 'Invalid' in list(set(getxln)):
                            exp = 'Not Match Found'
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, exp,
                                        results='FAILED',fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                            log.error('CASE[' + str(case) + '] ' + str(testcase) + ': FAILED')
                            self.fail('Invalid Item take place in list')
                        else:
                            exp = 'Match Found'
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, exp,
                                        results='PASSED',fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        sprints=sprints, incidentids=incidentids, alljson=alljson)
                            log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                            self.assert_('Actual Items in the list are valid and expected ')
        else:
            if 'Expected results given is not Matched' in str(getresults):
                get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, exresults, getresults,
                            results='FAILED', fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                            comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                log.error('Given expected results is not matched...')
                self.fail('Given expected results is not matched...')
            else:
                print('***********************************************************************************************')
                print('System_Response:' + str(getresults))
                print('***********************************************************************************************')
                print('Results:' + str(exresults))
                log.info('Expected_Result : ' + str(results))
                print('***********************************************************************************************')
                log.info('NTDATA....' + str(getresults) + '/ ' + str(exresults))
                self.compareresults(roles, testcase, var_types, getresults, tparams, exresults, case, xlcreate, tepoint,
                                    tpload, comments, timeelapsed, tparams, sprints, httpcodes, incidentids, eql='NO')

    def compareresults(self, roles, testcase, var_types, getresults, expresults, case, xlcreate, tepoint, tpload,
                       comments, timeelapsed, tparams, sprints, httpcodes, incidentids, alljson, eql='YES'):
        # comments_fail = 'Expected Results are not match with actual results'
        try:
            if eql == 'YES':
                if var_types == 'ST2':
                    gresults = getresults
                    if gresults == expresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, gresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                        self.assertEqual(gresults, expresults)
                    elif expresults in gresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, gresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                        self.assertIn(expresults, gresults, msg='Expected results available in Actual results')
                    else:
                        if httpcodes == 200:
                            httpcodes = 000
                            gresults = 'error found'
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, gresults,
                                    results='FAILED', fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.error('CASE[' + str(case) + '] ' + str(testcase) + ': FAILED')
                        self.assertEqual(gresults, expresults)
                elif var_types == 'ST5':
                    if expresults.startswith('*'):
                        expresults = getresults

                    if expresults == str({}):
                        if bool(getresults['metadata']):
                            getresults = getresults
                        else:
                            getresults = {}

                    if getresults == expresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                        self.assertEqual(getresults, expresults)
                    else:
                        expresults_list = ast.literal_eval(expresults)
                        if sorted(expresults_list) == sorted(getresults):
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                        results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        sprints=sprints, incidentids=incidentids, alljson=alljson)
                            log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                            self.assertEqual(sorted(getresults), sorted(expresults_list))
                        else:
                            if type(getresults) == list:
                                xrnt = []
                                for xget in range(0, len(getresults)):
                                    if expresults_list[xget] in getresults[xget] or getresults[xget] == \
                                            expresults_list[xget]:
                                        xrnt.append('Valid')
                                    else:
                                        xrnt.append('Invalid')

                                if 'Invalid' in list(set(xrnt)):
                                    self.assertFalse(expresults_list, getresults)
                                else:
                                    get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults,
                                                getresults,
                                                results='PASSED', fontx='35FC03', httpcodes=httpcodes,
                                                elapsed_secs=timeelapsed, sprints=sprints, incidentids=incidentids, alljson=alljson)
                                    log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                                    self.assertTrue(expresults_list, getresults)
                            else:
                                if expresults_list == {}:
                                    self.xFail(getresults)
                                else:
                                    self.assertFalse(expresults_list, getresults)
                else:
                    if getresults == expresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                        self.assertEqual(getresults, expresults)
                    elif expresults in getresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                        self.assertIn(expresults, getresults, msg='Expected results available in Actual results')
                    else:
                        self.assertFalse(getresults, expresults)
            else:
                if var_types == 'ST2':
                    if 'Key_Not_Found' in getresults:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                        self.assertNotIn(getresults, expresults)
                        log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                    else:
                        gtr = []
                        for xlen in range(0, len(getresults)):
                            print(getresults[xlen])
                            if getresults[xlen] == expresults:
                                self.assertEqual(getresults[xlen], expresults)
                                log.success('CASE[' + str(case) + '] ' + str(testcase) + ': PASSED')
                                results = 'PASSED'
                                gtr.append(results)
                            else:
                                self.assertEqual(getresults[xlen], expresults)
                                log.success('CASE[' + str(case) + '] ' + str(testcase) + ': FAILED')
                                results = 'PASSED'
                                gtr.append(results)

                        if 'FAILED' in gtr:
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                        results='FAILED', fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                        else:
                            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                        results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                        sprints=sprints, incidentids=incidentids, alljson=alljson)
                else:
                    resultsxx = None
                    for xamx in getresults:
                        for key, value in xamx.items():
                            print(key, value)
                            getvalue = str(key) + '--' + str(value)
                            print(getvalue)
                            print(expresults)
                            if expresults == getvalue:
                                resultsxx = 'FAILED'
                                self.assertNotEqual(getvalue, expresults)
                                break
                            elif expresults == str(key) or expresults in str(key):
                                resultsxx = 'FAILED'
                                self.assertNotEqual(getvalue, expresults)
                                break
                            elif expresults == str(value) or expresults in str(value):
                                resultsxx = 'FAILED'
                                self.assertNotEqual(getvalue, expresults)
                                break
                            else:
                                resultsxx = 'PASSED'
                                self.assertNotEqual(getvalue, expresults)
                    if resultsxx == 'FAILED':
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                    results='FAILED', fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
                    else:
                        get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, getresults,
                                    results='PASSED', fontx='35FC03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                                    sprints=sprints, incidentids=incidentids, alljson=alljson)
                    log.success('CASE[' + str(case) + '] ' + str(testcase) + ': ' + str(resultsxx))
        except Exception as e:
            gresults = str(getresults)+' : Not Match with expected :'+str(expresults)+'/ Failures or Errors : '+str(e)
            get_results(xlcreate, roles, testcase, tepoint, tpload, tparams, expresults, gresults, results='FAILED',
                        fontx='FC2C03', httpcodes=httpcodes, elapsed_secs=timeelapsed,
                        comments=comments, sprints=sprints, incidentids=incidentids, alljson=alljson)
            self.xFail(str(e))