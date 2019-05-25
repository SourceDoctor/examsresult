
DIVISOR_PRECISION = 2


class Calculation(object):

    def __init__(self, dbh, config, lng, data):
        self.dbh = dbh
        self.config = config
        self.lng = lng
        self.data = data

        self.result_reset()

    def result_reset(self):
        self.result_output_list = []
        self.result_output_count = 1

    def examslist_schoolclass(self, schoolyear, schoolclass, student_id, subject, timeperiod_id):
        result_list = []
        exams = self.dbh.get_exams(schoolyear, schoolclass, subject, timeperiod_id)
        for x in exams:
            exam_id = x[0]
            result_list.extend(self.examslist_student(exam_id=exam_id,
                                                  student_id=student_id,
                                                  subject=subject,
                                                  timeperiod_id=timeperiod_id))
        return result_list

    def examslist_student(self, student_id, subject, timeperiod_id, exam_id=None):
        return self.dbh.get_exam_result(exam_id=exam_id,
                                       student_id=student_id,
                                       subject=subject,
                                       timeperiod_id=timeperiod_id)

    def calculate_period_results(self, result_list, period_name, period_id, print_details=False):
        result_sum = 0
        result_count = 0
        result_average = 0

        for r in result_list:
            # real exam results are Database Objects, Simulations are tuple
            # date
            try:
                result_date = r.exam.date
            except AttributeError:
                result_date = r[0]
            # timeperiod id
            try:
                result_period_id = r.exam.time_period
            except AttributeError:
                result_period_id = r[1]
            # exam id
            try:
                result_exam_id = r.exam.exam_type
            except AttributeError:
                result_exam_id = r[2]
            # result
            try:
                result = r.result
            except AttributeError:
                result = r[3]
            # comment
            try:
                result_comment = r.comment
            except AttributeError:
                result_comment = r[0]

            if result_period_id != period_id:
                continue

            x_t = self.dbh.get_examtype_by_id(result_exam_id)

            if result:
                result_sum += result * x_t.weight
                result_count += x_t.weight

            if print_details:
                self.result_output_list.append((self.result_output_count, result_date, period_name, x_t.name, result, "", result_comment))
                self.result_output_count += 1

        if result_count:
            result_average = round(float(result_sum) / result_count, DIVISOR_PRECISION)

        return result_sum, result_count, result_average

    def calculate_complete_results_parts(self, result_sum, result_count, result_average, period_weight):
        complete_sum = 0
        complete_count = 0

        if result_sum:
            if self.config['schoolyear_result_calculation_method'] == 'complete':
                complete_sum = result_sum * period_weight
                complete_count = result_count * period_weight
            elif self.config['schoolyear_result_calculation_method'] == 'timeperiod':
                complete_sum = result_average * period_weight
                complete_count = period_weight
            else:
                print("unknown calculation method")

        return complete_sum, complete_count

    def show_results_schoolclass(self, schoolyear, schoolclass, subject):

        self.result_reset()

        timeperiod_list = self.dbh.get_timeperiod()

        for student in self.dbh.get_students(schoolyear, schoolclass):
            student_id = student[0]
            student_lastname = student[1]
            student_firstname = student[2]
            student_real_schoolclass = student[3]
            student_image = student[5]

            try:
                if self.data['combined_class'] and self.data['combined_class'] != student_real_schoolclass:
                    continue
            except KeyError:
                pass

            name = "%s, %s" % (student_lastname, student_firstname)
            data_list = (self.result_output_count, name)
            complete_t_p_result_sum = 0
            complete_t_p_result_count = 0
            complete_t_p_result_average = 0

            for period in timeperiod_list:
                period_id = period[0]
                period_name = period[1]
                period_weight = period[2]

                results = self.examslist_schoolclass(schoolyear=schoolyear,
                                                     schoolclass=schoolclass,
                                                     student_id=student_id,
                                                     subject=subject,
                                                     timeperiod_id=period_id)

                t_p_result_sum, t_p_result_count, t_p_result_average = self.calculate_period_results(result_list=results,
                                                                                                     period_name=period_name,
                                                                                                     period_id=period_id)

                _complete_t_p_result_sum, _complete_t_p_result_count = self.calculate_complete_results_parts(t_p_result_sum,
                                                                                                             t_p_result_count,
                                                                                                             t_p_result_average,
                                                                                                             period_weight)
                complete_t_p_result_sum += _complete_t_p_result_sum
                complete_t_p_result_count += _complete_t_p_result_count
                data_list += (t_p_result_average,)

            if complete_t_p_result_count:
                complete_t_p_result_average = round(float(complete_t_p_result_sum) / complete_t_p_result_count,
                                                    DIVISOR_PRECISION)
            data_list += (complete_t_p_result_average, student_image)

            # print student result
            self.result_output_list.append(data_list)
            self.result_output_count += 1

        return self.result_output_list

    def show_results_student(self, student_id, subject, simulate_data=[]):

        self.result_reset()

        timeperiod_list = self.dbh.get_timeperiod()
        complete_t_p_result_sum = 0
        complete_t_p_result_count = 0
        complete_t_p_result_average = 0

        for period in timeperiod_list:
            period_id = period[0]
            period_name = period[1]
            period_weight = period[2]

            results = self.examslist_student(student_id=student_id, subject=subject, timeperiod_id=period_id)
            results.extend(simulate_data)

            t_p_result_sum, t_p_result_count, t_p_result_average = self.calculate_period_results(result_list=results,
                                                                                                 period_name=period_name,
                                                                                                 period_id=period_id,
                                                                                                 print_details=True)

            _complete_t_p_result_sum, _complete_t_p_result_count = self.calculate_complete_results_parts(t_p_result_sum,
                                                                                                         t_p_result_count,
                                                                                                         t_p_result_average,
                                                                                                         period_weight)
            complete_t_p_result_sum += _complete_t_p_result_sum
            complete_t_p_result_count += _complete_t_p_result_count
            # print Average
            self.result_output_list.append((self.result_output_count, "", period_name, "", "", t_p_result_average, ""))
            self.result_output_count += 1

        if complete_t_p_result_count:
            complete_t_p_result_average = round(float(complete_t_p_result_sum) / complete_t_p_result_count,
                                                DIVISOR_PRECISION)

        data_list = (self.result_output_count, "", self.lng['schoolyear'], "", "", complete_t_p_result_average, "")

        # print schoolyear
        self.result_output_list.append(data_list)

        return self.result_output_list
