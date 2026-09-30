package com.datastore.person.controller;

import com.datastore.person.pojo.Student;
import com.datastore.person.repository.StudentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@RestController
public class StudentController {

    private static final Logger logger = LoggerFactory.getLogger(StudentController.class);

    @Autowired
    StudentRepository studentRepository;

    @RequestMapping(method = RequestMethod.POST, path = "/student/post")
    private ResponseEntity<String> postStudent(@RequestBody Student student, HttpServletRequest request) {
        studentRepository.save(student);
        logger.info("Posted student to DB : {}", student.getName());
        return ResponseEntity.status(HttpStatus.OK).body("Student successfully posted.");
    }

    @RequestMapping(method = RequestMethod.GET, path = "/student/get/{name}")
    private ResponseEntity<Student> getStudent(@PathVariable("name") String name) {
        logger.info("Getting student by name : {}", name);
        return studentRepository.findByName(name)
                .map(student -> ResponseEntity.ok().body(student))
                .orElse(ResponseEntity.notFound().build());
    }

    @RequestMapping(method = RequestMethod.GET, path = "/student/all")
    private ResponseEntity<List<Student>> getAllStudents() {
        logger.info("Getting all students");
        List<Student> stuList = studentRepository.findAll();
        return ResponseEntity.status(HttpStatus.OK).body(stuList);
    }
}